#!/usr/bin/env python3
"""Build static data for the website."""
import json
from pathlib import Path
from venue_data.storage import load_venue_config
from venue_data.text_utils import get_next_months
import yaml
import logging

logger = logging.getLogger(__name__)

def build_website_data():
    """Build JSON data file for website consumption."""
    output = {
        "venues": {},
        "last_updated": "",  # Will be set by GitHub Actions
    }
    
    base_dir = Path("data/venue-data")
    website_dir = Path("website/data")
    website_dir.mkdir(exist_ok=True)
    
    # Process each city
    for city_dir in base_dir.iterdir():
        if not city_dir.is_dir():
            continue
            
        city = city_dir.name
        venues = load_venue_config(city_dir / "venues.yaml")
        
        for venue_key, venue_info in venues.items():
            venue_data = {
                "name": venue_info["name"],
                "description": venue_info.get("description", ""),
                "months": {}
            }
            
            # Load playlist data for each month
            venue_dir = city_dir / venue_key
            for month in get_next_months():
                playlist_file = venue_dir / f"playlist_{month}.yaml"
                if not playlist_file.exists():
                    continue
                    
                try:
                    with open(playlist_file) as f:
                        data = yaml.safe_load(f)
                        # Skip test playlists
                        if "[TEST]" in data.get("playlist_url", ""):
                            continue
                        venue_data["months"][month] = {
                            "playlist_url": data["playlist_url"]
                        }
                except Exception as e:
                    logger.error(f"Error processing {playlist_file}: {e}")
                    continue
            
            if venue_data["months"]:  # Only include venues with playlists
                output["venues"][venue_key] = venue_data
    
    # Write output file
    output_file = website_dir / "venues.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    
    logger.info(f"Built website data: {output_file}")
    return output_file

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    build_website_data() 