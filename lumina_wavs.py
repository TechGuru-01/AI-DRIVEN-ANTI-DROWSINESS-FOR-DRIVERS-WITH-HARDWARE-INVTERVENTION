import sounddevice as sd
import soundfile as sf

class PreDriveWavs:
    @staticmethod
    def Introduction(wav_file_path='audio/predrive/intro.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)  
        sd.wait() 
        
    @staticmethod
    def Instructions_before_assessment(wav_file_path='audio/predrive/intro2.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
    
    @staticmethod
    def welcome(wav_file_path='audio/predrive/welcomeDrive.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod
    def If_yawning(wav_file_path='audio/predrive/assessIfYawn.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod
    def If_drowsy(wav_file_path='audio/predrive/assessIfDrowsy.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod
    def assess_If_2(wav_file_path='audio/predrive/assessIf2.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod   
    def reassess1(wav_file_path='audio/predrive/reassess1.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod
    def reassess2(wav_file_path='audio/predrive/reassess2.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod    
    def passed(wav_file_path='audio/predrive/passed.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod   
    def failed1(wav_file_path='audio/predrive/failed1.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod   
    def failed2(wav_file_path='audio/predrive/failed2.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()

class DriveWavs:
    @staticmethod
    def welcome_to_drive(wav_file_path='audio/drive/welcomeDrive.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod
    def back_to_awake(wav_file_path='audio/drive/backAwake.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod
    def drive_drowsy(wav_file_path='audio/drive/assessIfDrowsy.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod   
    def hazard(wav_file_path='audio/drive/intervention.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod    
    def alarm(wav_file_path='audio/drive/alarm.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
       
    @staticmethod    
    def severe_alarm(wav_file_path='audio/drive/3000Hz.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod           
    def assess_severe(wav_file_path='audio/drive/assessIfSeverePassenger.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod    
    def yawn_alert(wav_file_path='audio/drive/earlysigns.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
    
class LockoutWavs:
    @staticmethod    
    def activate_lockout(wav_file_path='audio/drive/lockoutActivate.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod    
    def attempt1(wav_file_path='audio/attempts/attempt1.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod    
    def attempt2(wav_file_path='audio/attempts/attempt2.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod    
    def attempt3(wav_file_path='audio/attempts/attempt3.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod    
    def lockout_done(wav_file_path='audio/lockout/lockoutDone.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
        
    @staticmethod   
    def lockout_on_going(wav_file_path='audio/lockout/lockoutOnGoing.wav'):
        data, samplerate = sf.read(wav_file_path)
        sd.play(data, samplerate)
        sd.wait()
         