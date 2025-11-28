"""
Configuration module for Policy Navigator Agent
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create directories if they don't exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# aiXplain Configuration
AIXPLAIN_API_KEY = os.getenv("AIXPLAIN_API_KEY")
AIXPLAIN_TEAM_ID = os.getenv("AIXPLAIN_TEAM_ID")
AGENT_ID = os.getenv("AGENT_ID")
INDEX_ID = os.getenv("INDEX_ID")

# External API Keys
COURTLISTENER_API_KEY = os.getenv("COURTLISTENER_API_KEY")

# Integration Keys
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

# Application Settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Data sources
DATA_SOURCES = {
    "federal_register": "https://www.federalregister.gov/api/v1",
    "epa_regulations": "https://www.epa.gov/laws-regulations",
    "courtlistener": "https://www.courtlistener.com/api/rest/v3"
}

# Agent configuration
AGENT_CONFIG = {
    "embedding_model": "6734c55df127847059324d9e",  # OpenAI Text Embedding Batch
    "llm_id": "6646261c6eb563165658bbb1",  # Default LLM
    "chunk_size": 1000,
    "chunk_overlap": 100,
    "top_k": 5
}

# Validate critical configuration
if not AIXPLAIN_API_KEY:
    print("WARNING: AIXPLAIN_API_KEY not set. Please configure .env file.")
