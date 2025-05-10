"""Spotify artist search and track fetching functionality."""
import time
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class SpotifyArtistSearch:
    """Handles Spotify artist searching and top track fetching with rate limiting and retries."""
    
    def __init__(self, spotify_client, rate_limit: float = 0.5, max_retries: int = 3):
        """Initialize the artist search handler.
        
        Args:
            spotify_client: Initialized Spotify client
            rate_limit: Time to wait between API calls in seconds
            max_retries: Maximum number of retry attempts for failed calls
        """
        self.spotify = spotify_client
        self.rate_limit = rate_limit
        self.max_retries = max_retries

    def _search_single_artist(self, artist_name: str) -> Optional[str]:
        """Search for a single artist and return their Spotify ID.
        
        Args:
            artist_name: Name of the artist to search for
            
        Returns:
            Spotify artist ID if found, None otherwise
        """
        results = self.spotify.search(q=artist_name, type='artist', limit=1)
        if not results['artists']['items']:
            logger.warning(f"No results found for artist: {artist_name}")
            return None
            
        artist = results['artists']['items'][0]
        # Verify the match is reasonable
        if artist['name'].lower() != artist_name.lower():
            logger.warning(f"Best match for {artist_name} was {artist['name']} - skipping")
            return None
            
        return artist['id']

    def search_artists(self, artist_names: List[str]) -> Dict[str, Optional[str]]:
        """Search for multiple artists with retry logic.
        
        Args:
            artist_names: List of artist names to search for
            
        Returns:
            Dictionary mapping artist names to their Spotify IDs (or None if not found)
        """
        results = {}
        for artist in artist_names:
            for attempt in range(self.max_retries):
                try:
                    results[artist] = self._search_single_artist(artist)
                    time.sleep(self.rate_limit)  # Rate limiting
                    break
                except Exception as e:
                    if attempt == self.max_retries - 1:
                        logger.error(f"Failed to find {artist}: {str(e)}")
                        results[artist] = None
                    else:
                        logger.info(f"Retry {attempt + 1} for {artist}")
                        time.sleep(1)  # Longer delay between retries
        return results

    def get_top_tracks(self, artist_ids: List[str], market: str = 'US') -> Dict[str, List[str]]:
        """Fetch top tracks for multiple artists.
        
        Args:
            artist_ids: List of Spotify artist IDs
            market: Market to get top tracks for (default: 'US')
            
        Returns:
            Dictionary mapping artist IDs to lists of their top track IDs
        """
        results = {}
        for artist_id in artist_ids:
            for attempt in range(self.max_retries):
                try:
                    tracks = self.spotify.artist_top_tracks(artist_id, market)
                    results[artist_id] = [track['id'] for track in tracks['tracks']]
                    time.sleep(self.rate_limit)  # Rate limiting
                    break
                except Exception as e:
                    if attempt == self.max_retries - 1:
                        logger.error(f"Failed to get tracks for {artist_id}: {str(e)}")
                        results[artist_id] = []
                    else:
                        logger.info(f"Retry {attempt + 1} for {artist_id}")
                        time.sleep(1)  # Longer delay between retries
        return results 