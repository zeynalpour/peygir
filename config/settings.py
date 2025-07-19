# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DEFAULT_EXTEND_DEADLINE_MINUTES = 10
THRESHOLD_MINUTES=3
FETCH_INTERVAL_MINUTES=1 
DEFAULT_DEADLINE_MINUTES=1