from dotenv import load_dotenv
import os

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

FAKEYOU_USERNAME = os.getenv("FAKEYOU_USERNAME")
FAKEYOU_PASSWORD = os.getenv("FAKEYOU_PASSWORD")
