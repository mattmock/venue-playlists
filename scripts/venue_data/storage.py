import yaml
from datetime import datetime
from typing import List
import os
from pathlib import Path
import logging
from .models import ArtistEvent

logger = logging.getLogger(__name__)

def save_artists_to_file(venue_name: str, artist_events: List[ArtistEvent], month: str, output_dir: str = "data/venue-data/sf") -> str:
    """Save artists to a YAML file with timestamp in venue-specific directory."""
    venue_dir = get_venue_output_dir(venue_name, output_dir)
    filename = f"{venue_dir}/artists_{month}.yaml"
    
    # Deduplicate artists while preserving order
    seen = set()
    unique_events = []
    for event in artist_events:
        if event.name not in seen:
            seen.add(event.name)
            unique_events.append(event)
    
    data = {
        "venue": venue_name,
        "month": month,
        "artists": [event.name for event in unique_events],
        "updated": datetime.now().isoformat()
    }
    
    with open(filename, 'w') as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
    
    logger.info(f"Saved {len(unique_events)} unique artists to {filename}")
    return filename

def load_venue_config(config_path: str = None) -> dict:
    """Load venue configuration with validation."""
    if config_path is None:
        config_path = "data/venue-data/sf/venues.yaml"
        
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
            
        if not isinstance(config, dict):
            raise ValueError("Invalid config format - expected dictionary")
            
        if 'venues' not in config:
            raise ValueError("Config missing required 'venues' key")
            
        # Return just the venues dictionary, not the whole config
        return config['venues']
        
    except Exception as e:
        logger.error(f"Error loading venue config from {config_path}: {str(e)}")
        raise

def get_venue_output_dir(venue_key: str, base_dir: str = "data/venue-data/sf") -> str:
    """Get the output directory for a venue and ensure it exists."""
    output_dir = f"{base_dir}/{venue_key}"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir 

def needs_update(venue_key: str, month: str, output_dir: str) -> bool:
    """Check if venue data needs to be updated (older than 24 hours)."""
    artist_file = Path(output_dir) / venue_key / f"artists_{month}.yaml"
    playlist_file = Path(output_dir) / venue_key / f"playlist_{month}.yaml"
    
    if artist_file.exists() and not playlist_file.exists():
        return True
        
    if playlist_file.exists():
        playlist_time = datetime.fromtimestamp(playlist_file.stat().st_mtime)
        artist_time = datetime.fromtimestamp(artist_file.stat().st_mtime)
        
        if artist_time > playlist_time:
            return True
            
        time_since_update = datetime.now() - playlist_time
        return time_since_update.days >= 1
        
    return True