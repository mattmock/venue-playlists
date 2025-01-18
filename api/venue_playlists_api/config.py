"""API configuration."""
import os
from pathlib import Path

def find_project_root() -> str:
    """Find the project root directory.
    
    Strategy:
    1. Use VENUE_PLAYLISTS_ROOT env var if set
    2. Look for parent directory containing 'api', 'website', and 'data' directories
    3. Fallback to current working directory
    """
    if root := os.environ.get('VENUE_PLAYLISTS_ROOT'):
        return root
        
    # Start from this file's directory and walk up
    current = Path(__file__).resolve().parent
    while current != current.parent:
        # Check if this looks like our project root
        if all((current / d).exists() for d in ['api', 'website', 'data']):
            return str(current)
        current = current.parent
    
    return os.getcwd()

class Config:
    """Base configuration.
    
    Environment Variables:
        VENUE_PLAYLISTS_ROOT: Root directory of the project
        VENUE_DATA_DIR: Directory containing venue data
        
    If VENUE_DATA_DIR is not set, it defaults to <VENUE_PLAYLISTS_ROOT>/data/venue-data
    """
    
    # Find project root by looking for key directories
    PROJECT_ROOT = find_project_root()
    
    # Prioritize explicit VENUE_DATA_DIR, fallback to default project structure
    VENUE_DATA_DIR = os.environ.get(
        'VENUE_DATA_DIR',
        str(Path(PROJECT_ROOT) / "data" / "venue-data")
    )
    
    # Log the configuration for debugging
    if os.environ.get('FLASK_DEBUG'):
        print(f"Project Root: {PROJECT_ROOT}")
        print(f"Venue Data Directory: {VENUE_DATA_DIR}")
