from venue_data.main import process_venue
from venue_data.storage import load_venue_config
from pathlib import Path
import os
from typing import List

def get_city_dirs(base_dir: str = "data/venue-data") -> list[str]:
    """Get list of city directories under venue-data."""
    return [d.name for d in Path(base_dir).iterdir() if d.is_dir()]

def process_city(city: str, base_dir: str = "data/venue-data", force_venue: str = None, force_all: bool = False) -> None:
    """Process all venues for a specific city."""
    city_path = f"{base_dir}/{city}"
    config_path = f"{city_path}/venues.yaml"
    
    try:
        venues = load_venue_config(config_path)
        print(f"\nProcessing {city.upper()} venues:")
        print("-" * 40)
        
        for venue_key in venues.keys():
            if force_venue and venue_key != force_venue:
                print(f"Skipping {venue_key} - not forced venue")
                continue
                
            output_files = process_venue(venue_key, output_dir=city_path, force=bool(force_venue or force_all))
            print(f"\nProcessed {venue_key}. Results saved to:")
            for file in output_files:
                print(f"  - {file}")
                
    except Exception as e:
        print(f"Error processing {city} venues: {e}")

if __name__ == "__main__":
    try:
        cities = get_city_dirs()
        if not cities:
            print("No city directories found in data/venue-data/")
            exit(1)
            
        for city in cities:
            process_city(city)
            
    except Exception as e:
        print(f"Error processing cities: {e}")