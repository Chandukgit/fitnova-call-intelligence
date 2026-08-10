from app.ai.whisper.faster_whisper import get_whisper_engine


class WhisperService:

    def transcribe(
        self,
        audio_path: str,
    ):

        return get_whisper_engine().transcribe(
            audio_path
        )


whisper_service = WhisperService()
