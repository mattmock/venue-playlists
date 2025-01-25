from spotipy.oauth2 import SpotifyOAuth
import os
import logging
from pathlib import Path
from dotenv import load_dotenv, set_key

logger = logging.getLogger(__name__)

def setup_spotify_auth():
    """Get or create Spotify refresh token"""
    load_dotenv()
    
    logger.info("Setting up Spotify authentication...")
    
    # Log environment variables (safely)
    logger.debug("Client ID present: %s", bool(os.environ.get('SPOTIFY_CLIENT_ID')))
    logger.debug("Client Secret present: %s", bool(os.environ.get('SPOTIFY_CLIENT_SECRET')))
    logger.debug("Redirect URI: %s", os.environ.get('SPOTIPY_REDIRECT_URI'))
    
    try:
        auth_manager = SpotifyOAuth(
            client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
            client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET'),
            redirect_uri='http://localhost:8888/callback',
            scope='playlist-modify-public playlist-modify-private user-read-private',
            open_browser=True,
            show_dialog=True  # Force re-authentication
        )
        
        logger.info("Getting token info...")
        token_info = auth_manager.get_cached_token()
        if not token_info:
            logger.info("No cached token found, starting new auth flow...")
            auth_manager.get_access_token()
            token_info = auth_manager.get_cached_token()
        
        if not token_info:
            raise ValueError("Failed to get token info")
        
        refresh_token = token_info['refresh_token']
        logger.info("Successfully obtained refresh token")
        
        # Save to .env
        env_path = Path('.env')
        set_key(env_path, 'SPOTIFY_REFRESH_TOKEN', refresh_token)
        logger.info("Saved refresh token to .env file")
        
        return refresh_token
        
    except Exception as e:
        logger.error("Error in Spotify authentication: %s", str(e))
        raise 