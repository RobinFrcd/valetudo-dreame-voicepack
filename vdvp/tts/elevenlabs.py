from elevenlabs import ElevenLabs, save
from elevenlabs.types import VoiceSettings
from vdvp.constants import ELEVENLABS_API_KEY
from vdvp.tts.tts_client import TTSClient

TTS_MODEL = "eleven_multilingual_v2"


class ElevenLabsClient(TTSClient):
    def __init__(self):
        super().__init__(output_format="mp3")
        self._client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    def _generate_audio(self, text: str, voice_id: str, file_path: str) -> None:
        mp3 = self._client.text_to_speech.convert(
            voice_id=voice_id,  # The parameter is voice_id
            text=text,
            model_id=TTS_MODEL,  # Or "eleven_mono_v1"
            output_format="mp3_44100_128",
            voice_settings=VoiceSettings(
                speed=1,
                style=0.9,
                similarity_boost=0.9,
                use_speaker_boost=True,
                stability=0.9,
            ),
        )
        save(mp3, file_path)
