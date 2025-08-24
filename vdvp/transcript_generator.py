import os
import csv
from elevenlabs.client import ElevenLabs
from tqdm import tqdm
from vdvp.constants import ELEVENLABS_API_KEY
import click

STT_MODEL = "scribe_v1"


def ogg_to_str(el_client: ElevenLabs, file_path: str) -> str:
    with open(file_path, "rb") as audio_file:
        response = el_client.speech_to_text.convert(file=audio_file, model_id=STT_MODEL)
        return response.text.strip()


def transcriptions_to_csv(transcriptions: list[tuple[str, str]], output_csv: str):
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(["filename", "transcript"])
        writer.writerows(transcriptions)
    print(f"\n✅ Transcription complete! Results saved to '{output_csv}'")


@click.command()
@click.option("--input-folder", type=click.Path(exists=True))
@click.option("--output-csv", type=click.Path())
def transcribe_ogg_folder(input_folder, output_csv):
    if not ELEVENLABS_API_KEY:
        print("Warning: ELEVENLABS_API_KEY is not set as an environment variable.")
        return

    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    ogg_files = sorted(
        [f for f in os.listdir(input_folder) if f.lower().endswith(".ogg")],
        key=lambda x: int(x.split(".")[0]),
    )
    if not ogg_files:
        print(f"Warning: No .ogg files found in '{input_folder}'.")
        return
    print(f"Found {len(ogg_files)} .ogg file(s) to process.")

    transcription_results = []

    for filename in tqdm(ogg_files, desc="Transcribing files"):
        file_path = os.path.join(input_folder, filename)

        if filename == "0.ogg":
            transcript_text = "Startup sound"
        elif filename == "200.ogg":
            transcript_text = "Shutdown sound"
        elif filename == "274.ogg":
            transcript_text = "Ding!"
        else:
            transcript_text = ogg_to_str(client, file_path)

        transcription_results.append([filename, transcript_text])

    transcriptions_to_csv(transcription_results, output_csv)
