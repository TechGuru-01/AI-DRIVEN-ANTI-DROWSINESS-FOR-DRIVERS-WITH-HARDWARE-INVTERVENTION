import os
import re
import time
import json
import numpy as np
import torch
import simpleaudio as sa
import pyaudio
from vosk import Model, KaldiRecognizer
from TTS.api import TTS

class LuminaChatbot:
    def __init__(
        self,
        name="Driver",
        vosk_model_path="model",
        tts_model="tts_models/en/ljspeech/tacotron2-DDC",
        device=None,
        sample_rate=16000,
        listen_timeout=5.0,
        tts_out="out/temp.wav"
    ):
        self.name = name
        self.sample_rate = sample_rate
        self.listen_timeout = listen_timeout
        self.tts_out = tts_out
        self.last_state = None

        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"[Lumina] device -> {self.device}")

        try:
            self.tts = TTS(model_name=tts_model)
            if hasattr(self.tts, "to"):
                try:
                    self.tts.to(self.device)
                except Exception:
                    pass
            print("[Lumina] TTS initialized.")
        except Exception as e:
            self.tts = None
            print(f"[Lumina][WARN] TTS initialization failed: {e}")

        if not os.path.exists(vosk_model_path):
            raise FileNotFoundError(f"Vosk model not found at '{vosk_model_path}'")
        self.vosk_model = Model(vosk_model_path)
        print("[Lumina] Vosk model loaded.")

        self._pyaudio = pyaudio.PyAudio()
        self._affirm_re = re.compile(r"\b(?:yes|yeah|yup|yep|sure|ok|okay|of course)\b", re.I)
        os.makedirs(os.path.dirname(self.tts_out) or ".", exist_ok=True)

    def speak(self, text, filename=None):
        filename = filename or self.tts_out
        if self.tts:
            try:
                self.tts.tts_to_file(text=text, file_path=filename)
                wave_obj = sa.WaveObject.from_wave_file(filename)
                play_obj = wave_obj.play()
                play_obj.wait_done()
            except Exception as e:
                print(f"[Lumina][Audio Error] {e}")
        else:
            print("[Lumina][TTS unavailable] would say:", text)

    def recognize_speech(self, timeout=None):
        timeout = timeout or self.listen_timeout
        recognizer = KaldiRecognizer(self.vosk_model, self.sample_rate)
        stream = self._pyaudio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=8192,
        )
        stream.start_stream()
        print("[Listening with Vosk...]")

        start_time = time.time()
        final_text = ""

        try:
            while time.time() - start_time < timeout:
                data = stream.read(4096, exception_on_overflow=False)
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    final_text = result.get("text", "").strip()
                    break
        except Exception as e:
            print(f"[Lumina][STT Error] {e}")
        finally:
            stream.stop_stream()
            stream.close()

        return final_text.lower()
    
    def _is_affirmative(self, text):
        return bool(text and self._affirm_re.search(text))

    def buzz_once(self, freq=1200, duration=0.2):
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        tone = np.sin(freq * t * 2 * np.pi)
        audio = (tone * 32767).astype(np.int16)
        sa.play_buffer(audio, 1, 2, sample_rate).wait_done()

    def buzz_pattern(self, sec=3, interval=0.5, freq=1200, duration=0.2):
        start = time.time()
        while time.time() - start < sec:
            self.buzz_once(freq=freq, duration=duration)
            time.sleep(interval)
