import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from .storage import (
    save_artists_to_file,
    load_venue_config,
    get_venue_output_dir,
    needs_update
)
from .models import ArtistEvent
from .scrapers import VenueScraper, BandsInTownScraper
from .scraper_factory import ScraperFactory
from .venue_processor import process_venue
from .openai_extractor import ArtistExtractor

# Create logs directory
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure logging format
log_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create file handler
file_handler = RotatingFileHandler(
    filename=log_dir / "venue_data.log",
    maxBytes=1024 * 1024,  # 1MB
    backupCount=5
)
file_handler.setFormatter(log_format)
file_handler.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
console_handler.setLevel(logging.INFO)

# Configure root logger
root_logger = logging.getLogger()
root_logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

# Configure package-specific loggers
logger = logging.getLogger(__name__)
logging.getLogger('venue_data.storage').setLevel(logging.INFO)
logging.getLogger('venue_data.scrapers.bandisintown').setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

__all__ = [
    'process_venue',
    'save_artists_to_file',
    'load_venue_config',
    'get_venue_output_dir',
    'needs_update',
    'ArtistEvent',
    'VenueScraper',
    'ScraperFactory',
    'ArtistExtractor'
] 