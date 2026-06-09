from states import DriverStates
from detection import LuminaDetection
import time
from systModes import SystemMode
import threading
from lumina_wavs import DriveWavs
from smsModule import SMSNotifier
from nodemcu import NodeMCUStates


class DriveINTVN:
    def __init__(self, detector: LuminaDetection, node: NodeMCUStates):
        self.detector = detector
        self.driver_state = DriverStates()
        self.chatbot = DriveWavs()
        self.mode = SystemMode.DRIVE.name
        self.running = True
        self.detector_thread = None
        self.node = node
        self.is_yawning_handled = False
        
    def observe_state(self, duration=0):
        start = time.time()
        observed_states = []
        drowsy_name = self.driver_state.state_1.name
        
        while time.time() - start < duration:
            raw_state = self.detector.get_last_state()
            if raw_state is not None:
                observed_states.append(raw_state) 
            time.sleep(0.1)                                 
      
        if not observed_states:
            return None
        
        drowsy_count = sum(1 for state in observed_states if state == drowsy_name)
        drowsy_percentage = (drowsy_count / len(observed_states)) * 100
        
        if drowsy_percentage >= 30:
            return drowsy_name
        
        return max(set(observed_states), key=observed_states.count)
        
    def assess_if_drowsy(self):
        self.chatbot.alarm('audio/drive/alarm.wav')
        self.chatbot.drive_drowsy('audio/drive/assessIfDrowsy.wav')
        self.chatbot.hazard('audio/drive/interventions.wav')
        self.node.send_state(3)
    
        while True:
            state = self.observe_state(5)
            if state in self.driver_state.state_1.name:
                self.node.send_state(3)
                self.chatbot.assess_severe('audio/drive/assessIfSeverePassenger.wav')
                self.chatbot.severe_alarm('audio/drive/3000.wav') 
                    
            elif state == self.driver_state.state_0.name:
                self.chatbot.back_to_awake('audio/drive/backAwake.wav')
                self.node.send_state(0)
                break
            
            else:
                time.sleep(0.3)
            
    def run(self):
        self.detector_thread = threading.Thread(target=self.detector.run, daemon=True)
        self.detector_thread.start()

        self.chatbot.welcome_to_drive('audio/drive/welcomeDrive (1).wav')
        
        while self.running:
            state = self.detector.get_last_state()
            self.driver_state.update(state)

            if state != self.driver_state.state_2.name:
                self.yawning_prompt = False
                

            if state == self.driver_state.state_0.name:
                time.sleep(0.1)

            elif state == self.driver_state.state_1.name:
                self.node.send_state(3)
                SMSNotifier.send_sms()
                self.assess_if_drowsy()
            elif state == self.driver_state.state_2.name: 
                self.chatbot.yawn_alert('audio/drive/earlysigns.wav')
                self.node.send_state(4)
                state = self.observe_state(5)
                if state == self.driver_state.state_1.name: 
                    self.node.send_state(3)
                    self.assess_if_drowsy()
                elif state == self.driver_state.state_0.name:
                    continue
                else:
                    continue
            else:
                time.sleep(0.3)