from venue_data.venue_processor import process_venue
from venue_data.storage import load_venue_config
import argparse
import logging
import sys
import os
from config.paths import VENUE_DATA_DIR, LOGS_DIR

# Ensure log directory exists
os.makedirs(LOGS_DIR, exist_ok=True)

# Set up logging to match API configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(LOGS_DIR, 'collect_events.log'))
    ]
)
logger = logging.getLogger(__name__)

def process_city(city: str = "sf", force_venue: str = None, force_all: bool = False) -> None:
    """Process venues for a specific city."""
    logger.info(f"Processing {city.upper()} venues")
    
    venues = load_venue_config(city)
    
    # If force_venue specified, only process that venue
    if force_venue:
        if force_venue not in venues:
            logger.error(f"Venue {force_venue} not found")
            return
        venues = {force_venue: venues[force_venue]}
    
    # Ensure venue data directory exists
    venue_data_dir = os.path.join(VENUE_DATA_DIR, city)
    os.makedirs(venue_data_dir, exist_ok=True)
    
    for venue_key in venues:
        logger.info(f"Processing {venue_key}...")
        output_files = process_venue(
            venue_key, 
            output_dir=venue_data_dir,
            force=bool(force_venue or force_all)
        )
        
        if output_files:
            logger.info(f"Processed {venue_key}. Results saved to:")
            for file in output_files:
                logger.info(f"  - {file}")
        else:
            logger.warning(f"No output files generated for {venue_key}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", help="Force update for specific venue key")
    parser.add_argument("--force-all", action="store_true", help="Force update all venues")
    args = parser.parse_args()
    
    try:
        process_city(force_venue=args.force, force_all=args.force_all)
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        sys.exit(1)