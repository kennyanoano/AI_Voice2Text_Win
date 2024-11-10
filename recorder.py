import sounddevice as sd
import wavio
import tempfile

class Recorder:
    def __init__(self):
        self.samplerate = 8000
        self.channels = 1
        self.filename = None
        self.recording = None

    def start_recording(self):
        self.recording = sd.rec(int(self.samplerate * 60), samplerate=self.samplerate, channels=self.channels)
        sd.wait()

    def stop_recording(self):
        sd.stop()
        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        wavio.write(temp_wav.name, self.recording, self.samplerate, sampwidth=1)
        self.filename = temp_wav.name

    def get_audio_file(self):
        return self.filename