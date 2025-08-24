import typing
from vdvp.tts.tts_client import TTSClient
from vdvp.tts.elevenlabs import ElevenLabsClient
from vdvp.tts.fakeyou import FakeYouClient

__all__ = ["ElevenLabsClient", "FakeYouClient", "TTSClient"]

ClientTypes = typing.Literal["elevenlabs", "fakeyou"]
