import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Verify required environment variables are present
required_vars = ['SPOTIFY_CLIENT_ID', 'SPOTIFY_CLIENT_SECRET', 'SPOTIFY_REFRESH_TOKEN']
missing_vars = [var for var in required_vars if not os.environ.get(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

SPOTIFY_CONFIG = {
    'client_id': os.environ.get('SPOTIFY_CLIENT_ID'),
    'client_secret': os.environ.get('SPOTIFY_CLIENT_SECRET'),
    'refresh_token': os.environ.get('SPOTIFY_REFRESH_TOKEN'),
    'scope': 'playlist-modify-public'
}

# Debug prints (first 4 chars only)
print("\nConfig Values:")
print(f"client_id: {SPOTIFY_CONFIG['client_id'][:4]}...")
print(f"client_secret: {SPOTIFY_CONFIG['client_secret'][:4]}...")
print(f"refresh_token: {SPOTIFY_CONFIG['refresh_token'][:4]}...")

# Number of top tracks to include per artist
TRACKS_PER_ARTIST = 1