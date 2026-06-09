from detection import LuminaDetection
import time
from systModes import SystemMode
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from lumina_Json import read_json,write_json,update_lockout, is_lockout_active
from lumina_wavs import LockoutWavs

LOCKOUT_DURATIONS = {
    1: 6,
    2: 11,
    3: 16
}

COUNTDOWN_WAVS = {
    15: "audio/countDown/15.wav",
    14: "audio/countDown/14.wav",
    13: "audio/countDown/13.wav",
    12: "audio/countDown/12.wav",
    11: "audio/countDown/11.wav",
    10: "audio/countDown/10.wav",
    9: "audio/countDown/9.wav",
    8: "audio/countDown/8.wav",
    7: "audio/countDown/7.wav",
    6: "audio/countDown/6.wav",
    5: "audio/countDown/5.wav",
    4: "audio/countDown/4.wav",
    3: "audio/countDown/3.wav",
    2: "audio/countDown/2.wav",
    1: "audio/countDown/1.wav"
}

class lockoutManager():
    def __init__(self, detector: LuminaDetection, detector_thread=None, lockout_reason=None):
        self.mode = SystemMode.LOCKOUT.name
        self.running = True
        self.detector = detector
        self.detector_thread = detector_thread
        self.lockout_reason = lockout_reason
        self.lockout_cb = LockoutWavs()

    def get_remaining_lockout(self, duration_minutes):
        data = read_json()
        lockout = data["lockout"]
        if not lockout["timestamp"]:
            return 0

        old_time = datetime.strptime(lockout["timestamp"], "%Y-%m-%d %I:%M:%S %p")
        old_time = old_time.replace(tzinfo=ZoneInfo("Asia/Manila"))
        now = datetime.now(ZoneInfo("Asia/Manila"))

        elapsed = now - old_time
        remaining = duration_minutes - elapsed.total_seconds() / 60
        return max(0, int(remaining))

    def run_lockout(self):
        while self.running and self.mode == SystemMode.LOCKOUT.name:
            data = read_json()
            lockout = data["lockout"]
            attempts = lockout.get("attempts",0)
            
            if attempts == 0:
                self.mode = SystemMode.PRE_DRIVE.name
                break
            
            if not is_lockout_active():
                attempts = lockout.get("attempts", 0) + 1
                attempts = min(attempts, 3)
                
                update_lockout(attempts=attempts, lockout_reason=self.lockout_reason)
                data = read_json()
                duration = LOCKOUT_DURATIONS[attempts]
                self.lockout_cb.activate_lockout('lockoutActivate.wav')
                
                if attempts == 1:
                    self.lockout_cb.attempt1('audio/attempts/attempt1.wav')
                elif attempts == 2:
                    self.lockout_cb.attempt2('audio/attempts/attempt2.wav')
                elif attempts >= 3:
                    self.lockout_cb.attempt3('audio/attempts/attempt3.wav')    

            else:
                attempts = lockout.get("attempts", 1)
                lookup_key = min(attempts, 3)
                duration = LOCKOUT_DURATIONS.get(lookup_key, 6)
                print(f"Debug: Real Attempt: {attempts}, Lookup: {lookup_key}, Duration: {duration}")

            remaining = self.get_remaining_lockout(duration)

            if remaining > 0:
                while remaining > 0:
                    if remaining in COUNTDOWN_WAVS:
                        self.lockout_cb.lockout_on_going(COUNTDOWN_WAVS[remaining])
                    else:
                        self.lockout_cb.lockout_on_going('audio/lockout/lockoutOnGoing.wav')
                    time.sleep(60)  
                    remaining = self.get_remaining_lockout(duration)
            else:
                if not lockout.get("lockout_handled", False):
                    self.lockout_cb.lockout_done('audio/lockout/lockoutDone.wav')
                    self.mode = SystemMode.PRE_DRIVE.name
                    lockout["lockout_handled"] = True
                    write_json(data)
                    break