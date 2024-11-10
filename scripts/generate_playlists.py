from pathlib import Path
from venue_data.storage import load_venue_config
from venue_data.text_utils import get_next_months
from playlist_data.generator import PlaylistGenerator
from playlist_data.storage import save_playlist_info
import yaml
import time

def load_artists_for_month(venue_key: str, month: str, city_path: str) -> list:
    """Load artists from venue's monthly YAML file."""
    filepath = Path(city_path) / venue_key / f"artists_{month}.yaml"
    if not filepath.exists():
        return []
    
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)
        return data.get('artists', [])

def process_city_playlists(city: str):
    """Create playlists for all venues in a city."""
    base_dir = "data/venue-data"
    city_path = f"{base_dir}/{city}"
    venues = load_venue_config(f"{city_path}/venues.yaml")
    generator = PlaylistGenerator()
    
    for month in get_next_months():
        print(f"\nProcessing playlists for {month}:")
        print("-" * 40)
        
        for venue_key in venues.keys():
            artists = load_artists_for_month(venue_key, month, city_path)
            if not artists:
                continue
            
            all_tracks = []
            for artist in artists:
                tracks = generator.search_artist_top_tracks(artist)
                all_tracks.extend(tracks)
                time.sleep(0.5)  # 500ms delay between artist searches
            
            if all_tracks:
                playlist_url = generator.create_venue_playlist(venue_key, month, all_tracks)
                if playlist_url:
                    save_playlist_info(venue_key, month, playlist_url, city_path)
                    print(f"Created playlist for {venue_key}: {playlist_url}")
                    time.sleep(1)  # 1 second delay between playlist creations

def generate_playlists():
    cities = [d.name for d in Path("data/venue-data").iterdir() if d.is_dir()]
    for city in cities:
        process_city_playlists(city)

if __name__ == "__main__":
    generate_playlists()