import os
import csv
import click
from tqdm import tqdm

from vdvp.tts import ClientTypes, TTSClient, ElevenLabsClient, FakeYouClient

CLIENT_MAP: dict[ClientTypes, type[TTSClient]] = {
    "elevenlabs": ElevenLabsClient,
    "fakeyou": FakeYouClient,
}


@click.command()
@click.option("--csv", "csv_path", type=click.Path(exists=True))
@click.option("--output", type=click.Path())
@click.option("--voice-id", type=str)
@click.option(
    "--client", "client_type", type=click.Choice(list(CLIENT_MAP.keys())), required=True
)
def csv_to_audio(csv_path: str, output: str, voice_id: str, client_type: ClientTypes):
    client: TTSClient = CLIENT_MAP[client_type]()

    os.makedirs(output, exist_ok=True)

    with open(csv_path, mode="r", encoding="utf-8") as csvfile:
        reader = list(csv.DictReader(csvfile))

        for index, row in tqdm(enumerate(reader), total=len(reader)):
            filename = row.get("filename")
            transcript = row.get("transcript")

            if not filename or not transcript:
                print(
                    f"⚠️ Warning: Skipping row {index + 2} due to missing filename or transcript."
                )
                continue

            client.generate_audio(
                text=transcript,
                voice_id=voice_id,
                output_dir=output,
                file_id=filename.split(".")[0],
            )
