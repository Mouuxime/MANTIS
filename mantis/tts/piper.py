import subprocess
import tempfile
import winsound
import os

from mantis.tts.utils import normalize_tts_text

class PiperTTS:
    def __init__(self, piper_path: str, model_path: str):
        self.piper_path = piper_path
        self.model_path = model_path

    def speak(self, text: str):
        text = normalize_tts_text(text)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            wav_path = f.name

        try:
            process = subprocess.Popen(
                [
                    self.piper_path,
                    "--model", self.model_path,
                    "--output_file", wav_path
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text=True
            )

            process.communicate(text)

            winsound.PlaySound(wav_path, winsound.SND_FILENAME)
    
        finally:
            try:
                os.remove(wav_path)
            except OSError:
                pass