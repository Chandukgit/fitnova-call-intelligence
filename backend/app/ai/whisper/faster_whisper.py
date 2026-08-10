from faster_whisper import WhisperModel

from app.ai.whisper.base import WhisperBase


class FasterWhisper(WhisperBase):

    def __init__(self):

        print("Loading Faster-Whisper model...")

        self.model = WhisperModel(
            model_size_or_path="base",
            device="cpu",
            compute_type="int8",
        )

        print("Faster-Whisper loaded successfully.")

    def transcribe(
        self,
        audio_path: str,
    ) -> dict:

        segments, info = self.model.transcribe(
            audio_path
        )

        transcript = []
        full_text = ""

        for segment in segments:

            transcript.append(
                {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip(),
                }
            )

            full_text += segment.text + " "

        return {
            "text": full_text.strip(),
            "language": info.language,
            "language_probability": info.language_probability,
            "segments": transcript,
        }


_whisper_engine: FasterWhisper | None = None


def get_whisper_engine() -> FasterWhisper:
    """Create the local model only when transcription is requested."""
    global _whisper_engine

    if _whisper_engine is None:
        _whisper_engine = FasterWhisper()

    return _whisper_engine
