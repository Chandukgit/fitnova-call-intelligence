from abc import ABC, abstractmethod


class WhisperBase(ABC):
    @abstractmethod
    def transcribe(self, audio_path: str) -> dict:
        """Convert an audio file into text."""
        pass
