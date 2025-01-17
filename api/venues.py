from flask import Blueprint, jsonify
import yaml
from pathlib import Path

bp = Blueprint('venues', __name__)

def load_venues(base_dir=None):
    """Load venue data from YAML files."""
    if base_dir is None:
        base_dir = Path("data/venue-data")
    else:
        base_dir = Path(base_dir)
    
    output = {"venues": {}}
    
    # Process each city
    for city_dir in base_dir.iterdir():
        if not city_dir.is_dir():
            continue
            
        # Load venue config
        with open(city_dir / "venues.yaml") as f:
            venues = yaml.safe_load(f)['venues']
            
        for venue_key, venue_info in venues.items():
            venue_data = {
                "name": venue_info["name"],
                "description": venue_info.get("description", ""),
                "months": {}
            }
            
            # Add to output
            output["venues"][venue_key] = venue_data
    
    return output

@bp.route('/venues')
def get_venues():
    """Return all venues and their playlists."""
    return jsonify(load_venues())
