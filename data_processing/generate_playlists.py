#!/usr/bin/env python3
"""Script to generate Spotify playlists for venues."""
from pathlib import Path
import yaml
import time
import argparse
import logging
import sys
import os
from typing import List, Dict, Any, Optional

from venue_data.storage import load_venue_config, needs_update
from venue_data.text_utils import get_next_months
from playlist_data.generator import PlaylistGenerator
from playlist_data.storage import save_playlist_info
from config.paths import VENUE_DATA_DIR, LOGS_DIR
from venue_data.playlist_cleanup import PlaylistCleaner

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
file_handler = logging.FileHandler(os.path.join(LOGS_DIR, 'generate_playlists.log'))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Prevent propagation to root logger to avoid duplicate logs
logger.propagate = False

def load_artists_for_month(venue_key: str, month: str, city_path: str) -> List[str]:
    """Load artists from venue's monthly YAML file.
    
    Args:
        venue_key: The venue identifier
        month: Month in format 'Month_YYYY'
        city_path: Path to city directory
        
    Returns:
        List of artist names
    """
    filepath = Path(city_path) / venue_key / f"artists_{month}.yaml"
    if not filepath.exists():
        logger.warning(f"No artist file found for {venue_key} in {month}")
        return []
    
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
            return data.get('artists', [])
    except Exception as e:
        logger.error(f"Error loading artists for {venue_key}: {str(e)}")
        return []

def process_city_playlists(
    city: str,
    generator: PlaylistGenerator,
    force_venue: Optional[str] = None,
    force_all: bool = False,
    test_venues: Optional[List[str]] = None,
    months_limit: Optional[int] = None,
    created_playlists: Optional[List[str]] = None
) -> None:
    """Create playlists for all venues in a city.
    
    Args:
        city: City identifier (e.g., 'sf')
        generator: Configured PlaylistGenerator instance
        force_venue: If set, only process this specific venue
        force_all: If True, force update all playlists
        test_venues: If set, only process these venues
        months_limit: If set, only process this many months
        created_playlists: List to track created playlist IDs
    """
    city_path = os.path.join(VENUE_DATA_DIR, city)
    logger.info(f"Processing playlists for {city.upper()}")
    
    try:
        venues = load_venue_config(city)
        
        # Filter venues if test_venues is specified
        if test_venues:
            venues = {k: v for k, v in venues.items() if k in test_venues}
            logger.info(f"Testing with venues: {', '.join(venues.keys())}")
        
        # Get months and limit if specified
        months = get_next_months()
        if months_limit:
            months = months[:months_limit]
            logger.info(f"Testing with {months_limit} months: {', '.join(months)}")
        
        for month in months:
            logger.info(f"Processing playlists for {month}")
            
            for venue_key, venue_info in venues.items():
                if force_venue and venue_key != force_venue:
                    continue
                    
                # Skip if playlist is up to date and not forced
                if not (force_venue or force_all) and not needs_update(venue_key, month, city_path):
                    logger.info(f"Skipping {venue_info['name']} - playlist is up to date")
                    continue
                    
                artists = load_artists_for_month(venue_key, month, city_path)
                if not artists:
                    logger.warning(f"No artists found for {venue_info['name']} in {month}")
                    continue
                
                logger.info(f"Found {len(artists)} artists for {venue_info['name']}")
                all_tracks = []
                for artist in artists:
                    tracks = generator.search_artist_top_tracks(artist)
                    if not tracks:
                        logger.warning(f"No tracks found for artist: {artist}")
                    all_tracks.extend(tracks or [])
                    time.sleep(0.5)  # Rate limiting
                
                if all_tracks:
                    try:
                        playlist_url = generator.create_venue_playlist(venue_info['name'], month, all_tracks)
                        if playlist_url:
                            save_playlist_info(venue_key, month, playlist_url, city_path)
                            logger.info(f"Created playlist for {venue_info['name']}: {playlist_url}")
                            if created_playlists is not None:
                                playlist_id = playlist_url.split('/')[-1]
                                created_playlists.append(playlist_id)
                            time.sleep(1)  # Rate limiting
                    except Exception as e:
                        logger.error(f"Error creating playlist for {venue_info['name']}: {str(e)}")
                else:
                    logger.warning(f"No tracks found for any artists at {venue_info['name']} in {month}")
                    
    except Exception as e:
        logger.error(f"Error processing city {city}: {str(e)}")

def generate_playlists(
    test_mode: bool = False,
    test_venues: Optional[List[str]] = None,
    months_limit: Optional[int] = None,
    force_all: bool = False,
    preserve_test: bool = False
) -> None:
    """Generate playlists for all cities.
    
    Args:
        test_mode: If True, create playlists with [TEST] prefix
        test_venues: If set, only process these venues
        months_limit: If set, only process this many months
        force_all: If True, force update all playlists even if up to date
        preserve_test: If True, keep test playlists after creation (default: False)
    """
    logger.info("Starting playlist generation")
    
    # Create and configure generator
    generator = PlaylistGenerator()
    created_playlists = []  # Track playlists created in this run
    
    if test_mode:
        logger.info("Running in TEST mode")
        generator.playlist_prefix = "[TEST] "
        generator.include_creation_time = True
    
    try:
        cities = [d.name for d in Path(VENUE_DATA_DIR).iterdir() if d.is_dir()]
        for city in cities:
            process_city_playlists(
                city,
                generator=generator,
                test_venues=test_venues,
                months_limit=months_limit,
                force_all=force_all,
                created_playlists=created_playlists
            )
        
        # Clean up test playlists unless preserve_test is True
        if test_mode and not preserve_test and created_playlists:
            logger.info("Cleaning up test playlists...")
            cleaner = PlaylistCleaner(spotify_client=generator.sp)
            for playlist_id in created_playlists:
                if cleaner.cleanup_specific_playlist(playlist_id):
                    logger.info(f"Cleaned up test playlist: {playlist_id}")
                
    except Exception as e:
        logger.error(f"Error in playlist generation: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Spotify playlists for venues")
    parser.add_argument("--test-mode", action="store_true", 
                       help="Create playlists with [TEST] prefix")
    parser.add_argument("--test-venues", nargs="+", metavar="VENUE",
                       help="Only process these venues (e.g., the-independent the-fillmore)")
    parser.add_argument("--months", type=int, metavar="N",
                       help="Only process N months (default: all)")
    parser.add_argument("--force", action="store_true",
                       help="Force update all playlists even if up to date")
    parser.add_argument("--preserve-test", action="store_true",
                       help="Keep test playlists after creation (default: False)")
    args = parser.parse_args()
    
    generate_playlists(
        test_mode=args.test_mode,
        test_venues=args.test_venues,
        months_limit=args.months,
        force_all=args.force,
        preserve_test=args.preserve_test
    )