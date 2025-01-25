from spotipy.oauth2 import SpotifyOAuth
import os
from pathlib import Path
from dotenv import load_dotenv, set_key

def setup_spotify_auth():
    """Get or create Spotify refresh token"""
    load_dotenv()
    
    auth_manager = SpotifyOAuth(
        client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
        client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET'),
        redirect_uri='http://localhost:8888/callback',
        scope='playlist-modify-public',
        open_browser=True
    )
    
    token_info = auth_manager.get_cached_token()
    if not token_info:
        auth_manager.get_access_token()
        token_info = auth_manager.get_cached_token()
    
    refresh_token = token_info['refresh_token']
    
    # Save to .env
    env_path = Path('.env')
    set_key(env_path, 'SPOTIFY_REFRESH_TOKEN', refresh_token)
    
    return refresh_token 