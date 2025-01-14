import os
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from .storage import load_venue_config, save_artists_to_file
from .text_utils import get_next_months, chunk_message
from .scraper import fetch_venue_page, clean_calendar_text
from .artist_extractor import ArtistExtractor
from .scraper_factory import ScraperFactory

logger = logging.getLogger(__name__)

# Set log level from environment variable
log_level = os.environ.get('LOGLEVEL', 'INFO').upper()
logger.setLevel(log_level)

def process_venue(venue_key: str, output_dir: str = "data/venue-data/sf", force: bool = False) -> List[str]:
    """Process a venue and save its events."""
    try:
        # Load venue config with new structure - get just the venues dict
        venues = load_venue_config()  # This now returns just the venues dictionary
        
        if venue_key not in venues:
            logger.error(f"Venue '{venue_key}' not found in config")
            return []
            
        venue_info = venues[venue_key]
        
        # Get appropriate scraper and fetch data
        try:
            scraper = ScraperFactory.get_scraper_for_venue(venue_info)
            artist_events = scraper.get_events(venue_key, venue_info)
            logger.info(f"Found {len(artist_events)} events for {venue_key}")
        except Exception as e:
            logger.error(f"Error getting events for {venue_key}: {str(e)}")
            return []
        
        if not artist_events:
            logger.warning(f"No events found for {venue_key}")
            return []
            
        # Process each month
        months = get_next_months()
        output_files = []
        for month in months:
            # Filter events for this month
            month_name = month.split('_')[0].lower()
            month_events = [
                event for event in artist_events 
                if event.date.strftime('%B').lower() == month_name
            ]
            
            if month_events:
                # Deduplicate artists while preserving order
                seen = set()
                unique_events = []
                for event in month_events:
                    if event.name not in seen:
                        seen.add(event.name)
                        unique_events.append(event)
                
                # Save unique artists for this month
                filename = save_artists_to_file(venue_key, unique_events, month, output_dir)
                output_files.append(filename)
                logger.info(f"Saved {len(unique_events)} unique artists for {month}")
            else:
                logger.warning(f"No artists found for {venue_key} in {month}")
        
        return output_files
        
    except Exception as e:
        logger.error(f"Error processing venue {venue_key}: {str(e)}")
        return [] 