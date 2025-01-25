import yaml
from pathlib import Path
from datetime import datetime

def save_playlist_info(venue_key: str, month: str, playlist_url: str, city_path: str):
    """Save playlist URL and metadata to YAML file."""
    output_dir = Path(city_path) / venue_key
    filename = output_dir / f"playlist_{month}.yaml"
    
    data = {
        'venue': venue_key,
        'month': month,
        'playlist_url': playlist_url,
        'created': datetime.now().isoformat()
    }
    
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(filename, 'w') as f:
        yaml.safe_dump(data, f, sort_keys=False) 