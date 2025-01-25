import os
import logging
from dotenv import load_dotenv

# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv(override=True)

# Only require client credentials initially
required_vars = ['SPOTIFY_CLIENT_ID', 'SPOTIFY_CLIENT_SECRET']
missing_vars = [var for var in required_vars if not os.environ.get(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

SPOTIFY_CONFIG = {
    'client_id': os.environ.get('SPOTIFY_CLIENT_ID'),
    'client_secret': os.environ.get('SPOTIFY_CLIENT_SECRET'),
    'refresh_token': os.environ.get('SPOTIFY_REFRESH_TOKEN'),
    'scope': 'playlist-modify-public'
}

# Log configuration status (safely)
logger.info("Spotify configuration loaded")
logger.debug("Required credentials present")
if SPOTIFY_CONFIG['refresh_token']:
    logger.debug("Refresh token found")
else:
    logger.debug("No refresh token - will be obtained during auth flow")

# Number of top tracks to include per artist
TRACKS_PER_ARTIST = 1