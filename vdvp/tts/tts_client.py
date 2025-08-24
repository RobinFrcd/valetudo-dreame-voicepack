from abc import ABC, abstractmethod
import os


class TTSClient(ABC):
    def __init__(self, output_format: str):
        self.output_format = output_format

    @abstractmethod
    def _generate_audio(self, text: str, voice_id: str, file_path: str) -> None:
        pass

    def generate_audio(
        self, text: str, voice_id: str, output_dir: str, file_id: str
    ) -> None:
        if not text.endswith(".") and not text.endswith("!"):
            text += "!"

        file_path = os.path.join(
            output_dir, self.output_format, f"{file_id}.{self.output_format}"
        )
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        self._generate_audio(text=text, voice_id=voice_id, file_path=file_path)
