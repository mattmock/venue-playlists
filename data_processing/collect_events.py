#!/usr/bin/env python3
"""Script to collect events from venue websites."""
from typing import Dict, Any, Optional, List
from venue_data.venue_processor import process_venue
from venue_data.storage import load_venue_config
import argparse
import logging
import sys
import os
from config.paths import VENUE_DATA_DIR, LOGS_DIR

# Ensure log directory exists
os.makedirs(LOGS_DIR, exist_ok=True)

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create formatters and handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File handler
file_handler = logging.FileHandler(os.path.join(LOGS_DIR, 'collect_events.log'))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Prevent propagation to root logger to avoid duplicate logs
logger.propagate = False

def process_city(
    city: str = "sf",
    force_venue: Optional[str] = None,
    force_all: bool = False,
    test_venues: Optional[List[str]] = None
) -> None:
    """Process venues for a specific city.
    
    Args:
        city: City to process venues for
        force_venue: If set, only process this specific venue
        force_all: If True, force update all venues
        test_venues: If set, only process these venues
    """
    logger.info(f"Starting event collection for {city.upper()}")
    
    try:
        # Load venue configuration - returns a dictionary of venue configs
        venues: Dict[str, Any] = load_venue_config(city)
        
        # Filter venues based on parameters
        if force_venue:
            if force_venue not in venues:
                logger.error(f"Venue {force_venue} not found in {city}")
                return
            venues = {force_venue: venues[force_venue]}
        elif test_venues:
            venues = {k: v for k, v in venues.items() if k in test_venues}
            if not venues:
                logger.error(f"No test venues found in {city}")
                return
            logger.info(f"Testing with venues: {', '.join(venues.keys())}")
        
        # Ensure venue data directory exists
        venue_data_dir = os.path.join(VENUE_DATA_DIR, city)
        os.makedirs(venue_data_dir, exist_ok=True)
        
        # Process each venue
        for venue_key, venue_info in venues.items():
            try:
                logger.info(f"Processing {venue_info.get('name', venue_key)}...")
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
                
    except Exception as e:
        logger.error(f"Error processing city {city}: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect events from venue websites")
    parser.add_argument("--force", help="Force update for specific venue key")
    parser.add_argument("--force-all", action="store_true", help="Force update all venues")
    parser.add_argument("--test-venues", nargs="+", metavar="VENUE",
                       help="Only process these venues (e.g., the-independent the-fillmore)")
    args = parser.parse_args()
    
    try:
        process_city(
            force_venue=args.force,
            force_all=args.force_all,
            test_venues=args.test_venues
        )
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        sys.exit(1)