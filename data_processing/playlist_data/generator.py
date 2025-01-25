from typing import List, Dict, Any, Optional
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from . import config
import time
from datetime import datetime

class PlaylistGenerator:
    """Generator for creating Spotify playlists."""
    
    playlist_prefix: str
    include_creation_time: bool
    sp: spotipy.Spotify
    
    def __init__(self, use_auth_handler: bool = True):
        """Initialize the playlist generator with Spotify authentication."""
        self.playlist_prefix = ""  # Prefix for playlist names (e.g. "[TEST] ")
        self.include_creation_time = False  # Whether to include creation time in playlist description
        
        if not config.SPOTIFY_CONFIG.get('refresh_token'):
            from . import auth
            auth.setup_spotify_auth()
            # Reload config after auth
            from importlib import reload
            reload(config)
        
        auth_manager = SpotifyOAuth(
            client_id=config.SPOTIFY_CONFIG['client_id'],
            client_secret=config.SPOTIFY_CONFIG['client_secret'],
            redirect_uri='http://localhost:8888/callback',
            scope=config.SPOTIFY_CONFIG['scope'],
            open_browser=use_auth_handler,
            cache_handler=None
        )
        
        # Set refresh token manually since the attribute is not exposed
        setattr(auth_manager, '_refresh_token', config.SPOTIFY_CONFIG['refresh_token'])
        
        try:
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            user = self.sp.me()
            if user and 'display_name' in user:
                print(f"\nAuthenticated as Spotify user: {user['display_name']}")
            else:
                print("\nAuthenticated with Spotify but couldn't get user details")
        except Exception as e:
            print("\nSpotify authentication failed!")
            print(f"Error: {str(e)}")
            raise
    
    def search_artist_top_tracks(self, artist_name: str, max_retries: int = 3) -> List[str]:
        """Search for an artist's top tracks and return their URIs."""
        for attempt in range(max_retries):
            try:
                results = self.sp.search(q=artist_name, type='artist', limit=1)
                if not results or 'artists' not in results or not results['artists']['items']:
                    return []
                
                artist_id = results['artists']['items'][0]['id']
                top_tracks = self.sp.artist_top_tracks(artist_id)
                
                if not top_tracks or 'tracks' not in top_tracks:
                    return []
                
                return [
                    track['uri'] 
                    for track in top_tracks['tracks'][:config.TRACKS_PER_ARTIST]
                    if 'uri' in track
                ]
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"Error finding tracks for {artist_name}: {str(e)}")
                    return []
                print(f"Retry {attempt + 1} for {artist_name}")
                time.sleep(1)  # Wait 1 second before retry
        return []  # Ensure we always return a list

    def create_venue_playlist(self, venue_name: str, month: str, track_uris: List[str]) -> str:
        """Create a Spotify playlist for a venue's monthly artists."""
        try:
            playlist_name = f"{self.playlist_prefix}{venue_name} - {month.replace('_', ' ').title()}"
            description = f"Top tracks from artists playing at {venue_name} in {month}"
            if self.include_creation_time:
                # Format timestamp in a more readable way and avoid newlines
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                description += f" (Created: {timestamp})"
            
            print(f"\nCreating playlist: {playlist_name}")
            print(f"Description: {description}")
            
            user_response = self.sp.me()
            if not user_response or 'id' not in user_response:
                raise ValueError("Could not get user ID")
                
            playlist = self.sp.user_playlist_create(
                user=user_response['id'],
                name=playlist_name,
                description=description
            )
            
            if not playlist:
                raise ValueError("Failed to create playlist")
            
            if track_uris and 'id' in playlist:
                for i in range(0, len(track_uris), 100):
                    batch = track_uris[i:i+100]
                    self.sp.playlist_add_items(playlist['id'], batch)
            
            # Get playlist URL from different fields
            if playlist and 'external_urls' in playlist and 'spotify' in playlist['external_urls']:
                return playlist['external_urls']['spotify']
            elif playlist and 'href' in playlist:
                return playlist['href']
            elif playlist and 'id' in playlist:
                return f"https://open.spotify.com/playlist/{playlist['id']}"
            else:
                raise ValueError("Could not get playlist URL")
            
        except Exception as e:
            print(f"Error creating playlist: {str(e)}")
            if 'playlist' in locals():
                print(f"Playlist data: {playlist}")
            return ""