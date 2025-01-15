from pathlib import Path
from venue_data.storage import load_venue_config, needs_update
from venue_data.text_utils import get_next_months
from playlist_data.generator import PlaylistGenerator
from playlist_data.storage import save_playlist_info
import yaml
import time
import argparse

def load_artists_for_month(venue_key: str, month: str, city_path: str) -> list:
    """Load artists from venue's monthly YAML file."""
    filepath = Path(city_path) / venue_key / f"artists_{month}.yaml"
    if not filepath.exists():
        return []
    
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)
        return data.get('artists', [])

def process_city_playlists(city: str, force_venue: str = None, force_all: bool = False):
    """Create playlists for all venues in a city."""
    base_dir = "data/venue-data"
    city_path = f"{base_dir}/{city}"
    venues = load_venue_config(f"{city_path}/venues.yaml")
    generator = PlaylistGenerator()
    
    for month in get_next_months():
        print(f"\nProcessing playlists for {month}:")
        print("-" * 40)
        
        for venue_key, venue_info in venues.items():
            if force_venue and venue_key != force_venue:
                continue
                
            # Skip if playlist is up to date and not forced
            if not (force_venue or force_all) and not needs_update(venue_key, month, city_path):
                print(f"Skipping {venue_info['name']} - playlist is up to date")
                continue
                
            artists = load_artists_for_month(venue_key, month, city_path)
            if not artists:
                print(f"No artists found for {venue_info['name']} in {month}")
                continue
            
            print(f"Found {len(artists)} artists for {venue_info['name']}")
            all_tracks = []
            for artist in artists:
                tracks = generator.search_artist_top_tracks(artist)
                if not tracks:
                    print(f"No tracks found for artist: {artist}")
                all_tracks.extend(tracks)
                time.sleep(0.5)
            
            if all_tracks:
                playlist_url = generator.create_venue_playlist(venue_info['name'], month, all_tracks)
                if playlist_url:
                    save_playlist_info(venue_key, month, playlist_url, city_path)
                    print(f"Created playlist for {venue_info['name']}: {playlist_url}")
                    time.sleep(1)
            else:
                print(f"No tracks found for any artists at {venue_info['name']} in {month}")

def generate_playlists():
    cities = [d.name for d in Path("data/venue-data").iterdir() if d.is_dir()]
    for city in cities:
        process_city_playlists(city)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-mode", action="store_true", 
                       help="Create playlists with [TEST] prefix")
    args = parser.parse_args()
    
    generator = PlaylistGenerator()
    
    # Modify playlist name in test mode
    if args.test_mode:
        generator.playlist_prefix = "[TEST] "
        generator.include_creation_time = True

if __name__ == "__main__":
    generate_playlists()