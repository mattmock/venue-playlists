from venue_data.main import process_venue
from venue_data.config import VENUES
import argparse

def update_all(city: str = "sf", force_venue: str = None, force_all: bool = False):
    # Process each venue
    for venue_key in VENUES:
        if force_venue and venue_key != force_venue:
            continue
            
        print(f"Processing venue: {venue_key}")
        process_venue(venue_key, force=force_all)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", help="Force update for specific venue key")
    parser.add_argument("--force-all", action="store_true", help="Force update all venues")
    args = parser.parse_args()
    
    update_all(force_venue=args.force, force_all=args.force_all) 