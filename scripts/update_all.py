#!/usr/bin/env python3
"""Script to update all venue data and playlists."""
import argparse
import logging
import sys
import os
from typing import Dict, Any, Optional
from venue_data.storage import load_venue_config
from venue_data.venue_processor import process_venue
from config.paths import VENUE_DATA_DIR, LOGS_DIR

# Ensure log directory exists
os.makedirs(LOGS_DIR, exist_ok=True)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Default to sys.stderr
        logging.FileHandler(os.path.join(LOGS_DIR, 'update_all.log'))
    ]
)
logger = logging.getLogger(__name__)

def update_all(city: str = "sf", force_venue: Optional[str] = None, force_all: bool = False) -> None:
    """Update all venue data and playlists.
    
    Args:
        city: City to process venues for
        force_venue: If set, only process this specific venue
        force_all: If True, force update all venues
    """
    logger.info(f"Starting update for {city.upper()} venues")
    
    # Load venue configuration - returns a dictionary of venue configs
    venues: Dict[str, Any] = load_venue_config(city)
    
    # Filter to specific venue if requested
    if force_venue:
        if force_venue not in venues:
            logger.error(f"Venue {force_venue} not found")
            return
        venues = {force_venue: venues[force_venue]}
    
    # Ensure venue data directory exists
    venue_data_dir = os.path.join(VENUE_DATA_DIR, city)
    os.makedirs(venue_data_dir, exist_ok=True)
    
    # Process each venue
    for venue_key in venues:
        logger.info(f"Processing venue: {venue_key}")
        try:
            output_files = process_venue(
                venue_key,
                output_dir=venue_data_dir,
                force=bool(force_venue or force_all)
            )
            
            if output_files:
                logger.info(f"Successfully processed {venue_key}. Files:")
                for file in output_files:
                    logger.info(f"  - {file}")
            else:
                logger.warning(f"No output files generated for {venue_key}")
                
        except Exception as e:
            logger.error(f"Error processing {venue_key}: {str(e)}")
            continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update all venue data and playlists")
    parser.add_argument("--force", help="Force update for specific venue key")
    parser.add_argument("--force-all", action="store_true", help="Force update all venues")
    args = parser.parse_args()
    
    try:
        update_all(force_venue=args.force, force_all=args.force_all)
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        sys.exit(1) 