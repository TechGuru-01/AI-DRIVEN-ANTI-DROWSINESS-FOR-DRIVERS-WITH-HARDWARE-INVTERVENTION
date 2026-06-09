import time
import threading
from states import DriverStates
from detection import LuminaDetection
from systModes import SystemMode, LockoutReason
from lumina_Json import update_lockout
from lumina_wavs import PreDriveWavs
from nodemcu import NodeMCUStates
class predriveEvaluator():
    def __init__(self,detector:LuminaDetection, node:NodeMCUStates):
        self.detector = detector
        self.mode = SystemMode.PRE_DRIVE.name
        self.driver_state = DriverStates()
        self.predrive_cb = PreDriveWavs()
        self.detector_thread = None
        self.node = node 
        self.running = True
        
    def observe_state(self, duration=0):
        start = time.time()
        observed_states = []
        drowsy_frames = self.driver_state.state_1.name
        yawn_frames = self.driver_state.state_2.name 
        
        while time.time() - start < duration:
            raw_state = self.detector.get_last_state()
            if raw_state is not None:
                observed_states.append(raw_state)
            time.sleep(0.2)
      
        if not observed_states:
            return None
        
        drowsy_count = sum(1 for state in observed_states if state == drowsy_frames)
        drowsy_percentage = (drowsy_count / len(observed_states)) * 100
        
        if drowsy_percentage>= 20:
            return drowsy_frames
        
        yawn_count = sum(1 for state in observed_states if state == yawn_frames)
        yawn_percentage = (yawn_count / len(observed_states)) * 100
        
        if yawn_percentage>= 10:
            return yawn_frames
        
        return max(set(observed_states), key=observed_states.count)

    def assess_if_awake(self):
        self.node.send_state(0)
        self.predrive_cb.passed('audio/predrive/passed.wav')
        return SystemMode.DRIVE.name
        
       
    def assess_if_drowsy(self):
        self.predrive_cb.If_drowsy('audio/predrive/assessIfDrowsy.wav')
        time.sleep(0.2)
        self.predrive_cb.reassess1('audio/predrive/reassess1.wav')
        time.sleep(3) 
        self.predrive_cb.reassess2('audio/predrive/reassess2.wav')
        time.sleep(0.2)

        state = self.observe_state(5)
        
        if state == self.driver_state.state_1.name:
            self.node.send_state(1)
            self.predrive_cb.failed1('audio/predrive/failed1.wav')
            time.sleep(0.2)
            self.predrive_cb.failed2('audio/predrive/failed2.wav')
            time.sleep(0.2)
            update_lockout(lockout_reason=LockoutReason.DROWSY_IN_AWAKE, lockout_handled=False, mode=SystemMode.LOCKOUT.name)
            if self.mode != SystemMode.LOCKOUT.name:
                self.mode = SystemMode.LOCKOUT.name
                return self.mode   
        elif state ==  self.driver_state.state_0.name: 
            self.node.send_state(0)
            self.predrive_cb.passed('audio/predrive/passed.wav')
            time.sleep(3) 
            if self.mode != SystemMode.DRIVE.name:
                self.mode = SystemMode.DRIVE.name
                return self.mode
        return self.mode 
           
        
            
    def run_predrive(self):
        self.detector_thread = threading.Thread(target=self.detector.run, daemon=True)
        self.detector_thread.start()
        predrive_cb = PreDriveWavs()
        self.node.send_state(0)
        time.sleep(3)
        PreDriveWavs.Introduction('audio/predrive/intro.wav')
        time.sleep(0.2)
        predrive_cb.Instructions_before_assessment('audio/predrive/intro2.wav')
        time.sleep(0.2)
        while self.running and self.mode == SystemMode.PRE_DRIVE.name:
            state = self.observe_state(10)
            if state is None:
                continue
            if state == self.driver_state.state_1.name:
                self.node.send_state(1)
                result = self.assess_if_drowsy()
                if result == SystemMode.DRIVE.name:
                    self.mode = SystemMode.DRIVE.name
                    return SystemMode.DRIVE.name
                elif result == SystemMode.LOCKOUT.name:
                    self.mode = SystemMode.LOCKOUT.name
                    return SystemMode.LOCKOUT.name
            
            elif state == self.driver_state.state_2.name:
                self.node.send_state(1)
                result = self.assess_if_drowsy()
                if result == SystemMode.DRIVE.name:
                    self.mode = SystemMode.DRIVE.name
                    return SystemMode.DRIVE.name
                elif result == SystemMode.LOCKOUT.name:
                    self.mode = SystemMode.LOCKOUT.name
                    return SystemMode.LOCKOUT.name

            elif state == self.driver_state.state_0.name:
                self.node.send_state(0)
                result = self.assess_if_awake()
                if result == SystemMode.DRIVE.name:
                    self.mode = SystemMode.DRIVE.name
                    return SystemMode.DRIVE.name

            time.sleep(1)   