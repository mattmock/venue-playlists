from venue_data.venue_processor import process_venue
from venue_data.storage import load_venue_config
from pathlib import Path
import argparse

def process_city(city: str = "sf", force_venue: str = None, force_all: bool = False) -> None:
    """Process venues for a specific city."""
    print(f"\nProcessing {city.upper()} venues:")
    print("-" * 40)
    
    venues = load_venue_config()
    
    # If force_venue specified, only process that venue
    if force_venue:
        if force_venue not in venues:
            print(f"Venue {force_venue} not found")
            return
        venues = {force_venue: venues[force_venue]}
    
    for venue_key in venues:
        print(f"\nProcessing {venue_key}...")
        output_files = process_venue(venue_key, force=bool(force_venue or force_all))
        
        print(f"\nProcessed {venue_key}. Results saved to:")
        for file in output_files:
            print(f"  - {file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", help="Force update for specific venue key")
    parser.add_argument("--force-all", action="store_true", help="Force update all venues")
    args = parser.parse_args()
    
    process_city(force_venue=args.force, force_all=args.force_all)