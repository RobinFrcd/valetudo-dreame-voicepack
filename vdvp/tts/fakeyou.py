import uuid
from vdvp.constants import FAKEYOU_USERNAME, FAKEYOU_PASSWORD
from vdvp.tts.tts_client import TTSClient
import time
import requests


class FakeYouClient(TTSClient):
    def __init__(self):
        super().__init__(output_format="wav")
        self._base_url = "https://api.fakeyou.com"
        self._session = requests.Session()
        self._session.headers.update(
            {"accept": "application/json", "content-Type": "application/json"}
        )

        self._login()

    def _login(self):
        response = self._session.post(
            f"{self._base_url}/login",
            json={"username_or_email": FAKEYOU_USERNAME, "password": FAKEYOU_PASSWORD},
        )
        response.raise_for_status()

    def _wait_for_job(self, job_token: str) -> bytes:
        while True:
            response = self._session.get(f"{self._base_url}/tts/job/{job_token}")
            if response.json()["state"]["status"] == "complete_success":
                wav_url = response.json()["state"]["maybe_public_bucket_wav_audio_path"]
                response = self._session.get(f"https://cdn-2.fakeyou.com{wav_url}")
                response.raise_for_status()
                return response.content
            time.sleep(5)

    def _generate_audio(self, text: str, voice_id: str, file_path: str) -> None:
        while True:
            try:
                data = {
                    # "uuid_idempotency_token": str(uuid.uuid5(uuid.NAMESPACE_DNS, text + voice_id)),
                    "uuid_idempotency_token": str(uuid.uuid4()),
                    "tts_model_token": voice_id,
                    "inference_text": text,
                }
                response = self._session.post(
                    f"{self._base_url}/tts/inference", json=data
                )
                response.raise_for_status()
                inference_job_token = response.json()["inference_job_token"]

                wav = self._wait_for_job(inference_job_token)

                with open(file_path, "wb") as f:
                    f.write(wav)

                return
            except Exception as e:
                print(f"Failed, {e}. Retrying in 5sec")
                time.sleep(5)
