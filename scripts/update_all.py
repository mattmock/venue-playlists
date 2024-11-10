from collect_events import process_city
from generate_playlists import process_city_playlists
from build_website_data import build_venue_data
import argparse

def update_all(city: str = "sf", force_venue: str = None, force_all: bool = False):
    # 1. Collect new events
    process_city(city, force_venue=force_venue, force_all=force_all)
    
    # 2. Generate playlists
    process_city_playlists(city, force_venue=force_venue, force_all=force_all)
    
    # 3. Build website data
    build_venue_data(city)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", help="Force update for specific venue key")
    parser.add_argument("--force-all", action="store_true", help="Force update all venues")
    args = parser.parse_args()
    
    update_all(force_venue=args.force, force_all=args.force_all) 