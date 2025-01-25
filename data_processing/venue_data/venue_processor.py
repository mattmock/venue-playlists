import os
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict
from .storage import load_venue_config, save_artists_to_file
from .text_utils import get_next_months
from .scraper_factory import ScraperFactory

logger = logging.getLogger(__name__)

# Set log level from environment variable
log_level = os.environ.get('LOGLEVEL', 'INFO').upper()
logger.setLevel(log_level)

def get_venue_info(venue_key: str) -> Optional[Dict]:
    """Get venue information from configuration.
    
    Args:
        venue_key: The key identifying the venue
        
    Returns:
        Dict containing venue configuration if found, None otherwise
    """
    venues = load_venue_config()
    venue_info = venues.get(venue_key)
    
    if not venue_info:
        logger.error(f"Venue '{venue_key}' not found in configuration")
        return None
        
    if not venue_info.get('scrapers'):
        logger.error(f"No scrapers configured for venue '{venue_key}'")
        return None
        
    return venue_info

def process_venue(venue_key: str, output_dir: Optional[str] = None, force: bool = False) -> List[str]:
    """Process a venue and extract artists for the next 3 months.
    
    Args:
        venue_key: The key identifying the venue
        output_dir: Optional directory to save output files (default: data/venue-data/sf)
        force: Whether to force processing even if data is up to date
        
    Returns:
        List of paths to generated files
    
    Raises:
        ValueError: If venue configuration is invalid
        RuntimeError: If processing fails
    """
    try:
        # Set default output directory if none provided
        if output_dir is None:
            output_dir = str(Path(__file__).parent.parent.parent / "data" / "venue-data" / "sf")

        # Get venue configuration
        venue_info = get_venue_info(venue_key)
        if not venue_info:
            raise ValueError(f"Invalid venue configuration for '{venue_key}'")

        output_files = []
        months = get_next_months()
        
        # Skip update check if force is True
        if not force:
            needs_processing = False
            for month in months:
                if venue_info.get('last_updated', datetime(1970, 1, 1)) < datetime.fromtimestamp(os.path.getctime(f"{output_dir}/{venue_key}_{month}_artists.txt")):
                    needs_processing = True
                    break
                    
            if not needs_processing:
                logger.info(f"Skipping {venue_key} - data is up to date")
                return []
            
        # Get appropriate scraper and fetch data
        scraper = ScraperFactory.get_scraper_for_venue(venue_info)
        if not scraper:
            raise ValueError(f"No suitable scraper found for venue '{venue_key}'")
            
        # Get events from venue
        artist_events = scraper.get_events(venue_key, venue_info)
        if not artist_events:
            logger.warning(f"No events found for venue '{venue_key}'")
            return []
            
        logger.info(f"Found {len(artist_events)} total artists for {venue_key}")
        
        # Save results for each month
        for month in months:
            if force or venue_info.get('last_updated', datetime(1970, 1, 1)) < datetime.fromtimestamp(os.path.getctime(f"{output_dir}/{venue_key}_{month}_artists.txt")):
                filename = save_artists_to_file(venue_key, artist_events, month, output_dir)
                output_files.append(filename)
                logger.debug(f"Saved {month} data to {filename}")
            
        return output_files
        
    except Exception as e:
        logger.error(f"Error processing venue {venue_key}: {e}")
        raise

if __name__ == "__main__":
    # Example usage with default SF venue
    output_files = process_venue("independent")
    print(f"Results saved to: {output_files}") 