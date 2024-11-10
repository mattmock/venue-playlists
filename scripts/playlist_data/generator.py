from typing import List
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from . import config
import time

class PlaylistGenerator:
    def __init__(self):
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
            open_browser=False,
            cache_handler=None
        )
        
        auth_manager.refresh_token = config.SPOTIFY_CONFIG['refresh_token']
        
        try:
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            user = self.sp.me()
            print(f"\nAuthenticated as Spotify user: {user['display_name']}")
        except Exception as e:
            print("\nSpotify authentication failed!")
            print(f"Error: {str(e)}")
            raise
    
    def search_artist_top_tracks(self, artist_name: str, max_retries: int = 3) -> List[str]:
        """Search for an artist's top tracks and return their URIs."""
        for attempt in range(max_retries):
            try:
                results = self.sp.search(q=artist_name, type='artist', limit=1)
                if not results['artists']['items']:
                    return []
                
                artist_id = results['artists']['items'][0]['id']
                top_tracks = self.sp.artist_top_tracks(artist_id)
                
                return [
                    track['uri'] 
                    for track in top_tracks['tracks'][:config.TRACKS_PER_ARTIST]
                ]
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"Error finding tracks for {artist_name}: {str(e)}")
                    return []
                print(f"Retry {attempt + 1} for {artist_name}")
                time.sleep(1)  # Wait 1 second before retry

    def create_venue_playlist(self, venue_name: str, month: str, track_uris: List[str]) -> str:
        """Create a Spotify playlist for a venue's monthly artists."""
        try:
            playlist_name = f"{venue_name} - {month.replace('_', ' ').title()}"
            playlist = self.sp.user_playlist_create(
                user=self.sp.me()['id'],
                name=playlist_name,
                description=f"Top tracks from artists playing at {venue_name} in {month}"
            )
            
            if track_uris:
                for i in range(0, len(track_uris), 100):
                    batch = track_uris[i:i+100]
                    self.sp.playlist_add_items(playlist['id'], batch)
            
            # Get playlist URL from different fields
            if 'external_urls' in playlist and 'spotify' in playlist['external_urls']:
                return playlist['external_urls']['spotify']
            elif 'href' in playlist:
                return playlist['href']
            else:
                print(f"Playlist response structure: {playlist.keys()}")
                return f"https://open.spotify.com/playlist/{playlist['id']}"
            
        except Exception as e:
            print(f"Error creating playlist: {str(e)}")
            if 'playlist' in locals():
                print(f"Playlist data: {playlist}")
            return ""