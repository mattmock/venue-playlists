from pathlib import Path
import yaml
import json
from venue_data.text_utils import get_next_months
from venue_data.storage import load_venue_config
from filelock import FileLock

def build_venue_data(city: str = "sf"):
    try:
        base_dir = Path(f"data/venue-data/{city}")
        venues_config = load_venue_config(base_dir / "venues.yaml")
        if not venues_config:
            raise ValueError(f"No venue config found for {city}")
            
        months = get_next_months()
        
        venue_data = []
        for venue_key, venue_info in venues_config.items():
            venue_entry = {
                "id": venue_key,
                "name": venue_info["name"],
                "months": []
            }
            
            for month in months:
                # Check for playlist
                playlist_file = base_dir / venue_key / f"playlist_{month}.yaml"
                if playlist_file.exists():
                    with open(playlist_file) as f:
                        playlist_data = yaml.safe_load(f)
                        venue_entry["months"].append({
                            "name": month,
                            "playlist_url": playlist_data["playlist_url"]
                        })
            
            venue_data.append(venue_entry)
        
        # Ensure website/data directory exists
        output_dir = Path("website/data")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{city}_venues.json"
        
        with FileLock(f"{output_file}.lock"):
            with open(output_file, 'w') as f:
                json.dump(venue_data, f, indent=2)
    except Exception as e:
        print(f"Error building website data: {e}")
        raise

if __name__ == "__main__":
    build_venue_data() 