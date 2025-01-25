import logging
from typing import List, Optional
from datetime import datetime, timedelta
import spotipy
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)

class PlaylistCleaner:
    """Utility for cleaning up test playlists."""
    
    def __init__(self, spotify_client: Optional[spotipy.Spotify] = None):
        """Initialize with optional spotify client."""
        self.sp = spotify_client or spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth())
        
    def cleanup_test_playlists(self, older_than_hours: int = 24) -> List[str]:
        """Clean up test playlists older than specified hours."""
        cleaned_playlists = []
        cutoff_time = datetime.now() - timedelta(hours=older_than_hours)
        
        # Get user's playlists
        playlists = self.sp.current_user_playlists()
        
        for playlist in playlists['items']:
            # Check if it's a test playlist (has [TEST] prefix)
            if playlist['name'].startswith('[TEST]'):
                # Get creation time from playlist description
                created_at = self._get_playlist_creation_time(playlist)
                if created_at and created_at < cutoff_time:
                    try:
                        self.sp.current_user_unfollow_playlist(playlist['id'])
                        cleaned_playlists.append(playlist['id'])
                        logger.info(f"Cleaned up test playlist: {playlist['name']} ({playlist['id']})")
                    except Exception as e:
                        logger.error(f"Failed to delete playlist {playlist['id']}: {e}")
        
        return cleaned_playlists
    
    def cleanup_specific_playlist(self, playlist_id: str) -> bool:
        """Clean up a specific playlist by ID."""
        try:
            self.sp.current_user_unfollow_playlist(playlist_id)
            logger.info(f"Cleaned up playlist: {playlist_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete playlist {playlist_id}: {e}")
            return False
    
    def _get_playlist_creation_time(self, playlist: dict) -> Optional[datetime]:
        """Extract creation time from playlist description."""
        try:
            description = playlist.get('description', '')
            if 'Created:' in description:
                time_str = description.split('Created:')[1].strip()
                return datetime.fromisoformat(time_str)
        except Exception:
            pass
        return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Clean up test playlists")
    parser.add_argument("--hours", type=int, default=24, 
                       help="Clean up playlists older than this many hours")
    parser.add_argument("--playlist-id", help="Clean up a specific playlist")
    args = parser.parse_args()
    
    cleaner = PlaylistCleaner()
    if args.playlist_id:
        cleaner.cleanup_specific_playlist(args.playlist_id)
    else:
        cleaner.cleanup_test_playlists(args.hours) 