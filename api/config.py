"""API configuration."""
import os
from pathlib import Path

class Config:
    """Base configuration."""
    
    # Default to project root/data/venue-data
    VENUE_DATA_DIR = os.environ.get(
        'VENUE_DATA_DIR',
        str(Path(__file__).parent.parent / "data" / "venue-data")
    )
