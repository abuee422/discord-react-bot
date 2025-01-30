from dotenv import load_dotenv
import os

load_dotenv()

# Discord credentials and configuration
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
if not AUTH_TOKEN:
    raise ValueError("Missing AUTH_TOKEN in environment variables")

CHANNEL_ID = os.getenv("CHANNEL_ID")
if not CHANNEL_ID:
    raise ValueError("Missing CHANNEL_ID in environment variables")

EMOJI = os.getenv("EMOJI", "✅")
