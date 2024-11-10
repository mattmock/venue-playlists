import yaml
from datetime import datetime
from typing import List
import os
from pathlib import Path
from .models import ArtistEvent

def save_artists_to_file(venue_name: str, artist_events: List[ArtistEvent], month: str, output_dir: str = "data/venue-data/sf") -> str:
    """Save artists to a YAML file with timestamp in venue-specific directory."""
    venue_dir = get_venue_output_dir(venue_name, output_dir)
    filename = f"{venue_dir}/artists_{month}.yaml"
    
    # Filter artists for this month
    month_date = datetime.strptime(month, "%B_%Y")
    month_artists = [
        event.name for event in artist_events 
        if event.date.strftime("%B_%Y").lower() == month.lower()
    ]
    
    data = {
        "venue": venue_name,
        "month": month,
        "artists": month_artists,
        "updated": datetime.now().isoformat()
    }
    
    with open(filename, 'w') as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
    
    return filename

def load_venue_config(config_path: str = "data/venue-data/sf/venues.yaml") -> dict:
    """Load venue configuration from YAML file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading venue config {config_path}: {e}")
        return {}

def get_venue_output_dir(venue_key: str, base_dir: str = "data/venue-data/sf") -> str:
    """Get the output directory for a venue and ensure it exists."""
    output_dir = f"{base_dir}/{venue_key}"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir 