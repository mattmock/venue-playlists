"""Project-wide path configuration."""
import os
from pathlib import Path

# Project directories - use the directory containing the config folder as project root
PROJECT_ROOT = os.getenv('VENUE_PLAYLISTS_ROOT', str(Path(__file__).parent.parent))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
VENUE_DATA_DIR = os.path.join(DATA_DIR, 'venue-data')
LOGS_DIR = os.path.join(PROJECT_ROOT, 'logs') 