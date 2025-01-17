from flask import Blueprint, jsonify, current_app
import yaml
from pathlib import Path
import logging
from datetime import datetime
from scripts.venue_data.text_utils import get_next_months

bp = Blueprint('venues', __name__)
logger = logging.getLogger(__name__)

def load_venues(base_dir=None):
    """Load venue data from YAML files."""
    if base_dir is None:
        base_dir = Path(current_app.config['VENUE_DATA_DIR'])
    else:
        base_dir = Path(base_dir)
    
    if not base_dir.exists():
        error_msg = f"Venue data directory not found: {base_dir}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    output = {
        "venues": {},
        "last_updated": datetime.now().isoformat()
    }
    
    # Process each city
    for city_dir in base_dir.iterdir():
        if not city_dir.is_dir():
            continue
            
        try:
            # Load venue config
            venue_config = city_dir / "venues.yaml"
            if not venue_config.exists():
                logger.warning(f"No venues.yaml found in {city_dir}")
                continue
                
            try:
                with open(venue_config) as f:
                    venues = yaml.safe_load(f)
                    if not venues or 'venues' not in venues:
                        logger.warning(f"Invalid venue config in {venue_config}")
                        continue
                    venues = venues['venues']
            except yaml.YAMLError as e:
                error_msg = f"Error parsing YAML in {venue_config}: {str(e)}"
                logger.error(error_msg)
                raise ValueError(error_msg)
                
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
                
                # Include all venues, even without playlists
                output["venues"][venue_key] = venue_data
                    
        except ValueError as e:
            # Re-raise YAML parsing errors to be handled by the endpoint
            raise
        except Exception as e:
            logger.error(f"Error processing city {city_dir}: {e}")
            continue
    
    return output

@bp.route('/venues')
def get_venues():
    """Return all venues and their playlists."""
    try:
        return jsonify(load_venues())
    except FileNotFoundError as e:
        logger.error(f"Venue data directory not found: {e}")
        return jsonify({"error": "Venue data not available"}), 503
    except ValueError as e:
        logger.error(f"YAML parsing error: {e}")
        return jsonify({"error": "Invalid venue data format"}), 500
    except Exception as e:
        logger.error(f"Error loading venues: {e}")
        return jsonify({"error": "Internal server error"}), 500
