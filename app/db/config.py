import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "google_api_key": os.getenv("GEMINI_API_KEY"),
    "chroma_path": "./atk_patterns_chroma",
    "collection_name": "attack_patterns",
    "batch_size": 50,
    "chunk_size": 800,
    "chunk_overlap": 80,
}
