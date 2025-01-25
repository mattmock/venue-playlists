"""API configuration."""
import os
from pathlib import Path
from typing import Optional, Dict, Any

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Venue data configuration
VENUE_DATA_DIR = str(os.getenv("VENUE_DATA_DIR", DATA_DIR / "venue-data"))
EXAMPLE_DATA_DIR = str(DATA_DIR / "examples")

# Ensure directories exist
os.makedirs(VENUE_DATA_DIR, exist_ok=True)
os.makedirs(EXAMPLE_DATA_DIR, exist_ok=True)

# API Configuration
FLASK_ENV = os.getenv("FLASK_ENV", "development")
DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"

# CORS Configuration
DEFAULT_ORIGINS = [
    "http://localhost:3000",  # Development frontend
    "http://localhost:8000",  # Local preview
]

if FLASK_ENV == "production":
    DEFAULT_ORIGINS = [
        "https://venue-playlists.vercel.app",
        "https://*.venue-playlists.vercel.app"
    ]

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", ",".join(DEFAULT_ORIGINS)).split(",")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = str(os.getenv("LOG_DIR", PROJECT_ROOT / "logs"))
os.makedirs(LOG_DIR, exist_ok=True)

# Documentation of paths
__doc__ = """
Configuration for the Venue Playlists API.

Directory Structure:
- VENUE_DATA_DIR: Active venue data (default: <PROJECT_ROOT>/data/venue-data)
- EXAMPLE_DATA_DIR: Example configurations (default: <PROJECT_ROOT>/data/examples)
- LOG_DIR: Application logs (default: <PROJECT_ROOT>/logs)

Environment Variables:
- VENUE_DATA_DIR: Override the default venue data directory
- LOG_DIR: Override the default log directory
- LOG_LEVEL: Set logging level (default: INFO)
- FLASK_ENV: Set environment (development/production)
- FLASK_DEBUG: Enable debug mode (1/0)
- ALLOWED_ORIGINS: Comma-separated list of allowed CORS origins
"""

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

class BaseConfig:
    """Base configuration class with shared settings.
    
    Environment Variables:
        VENUE_PLAYLISTS_ROOT: Root directory of the project
        VENUE_DATA_DIR: Directory containing venue data
        FLASK_ENV: The environment to run in (development/testing/production)
        
    If VENUE_DATA_DIR is not set, it defaults to <VENUE_PLAYLISTS_ROOT>/data/venue-data
    """
    
    # Find project root by looking for key directories
    PROJECT_ROOT: str = find_project_root()
    
    # Data directories
    VENUE_DATA_DIR: str = VENUE_DATA_DIR
    EXAMPLE_DATA_DIR: str = EXAMPLE_DATA_DIR
    LOG_DIR: str = LOG_DIR
    
    # Security settings
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'dev')
    
    # API settings
    API_VERSION: str = '1.0'
    
    # CORS settings
    CORS_ORIGINS: list[str] = ALLOWED_ORIGINS
    
    # Logging settings
    LOG_LEVEL: str = LOG_LEVEL
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    
    DEBUG: bool = True
    TESTING: bool = False
    LOG_LEVEL = 'DEBUG'
    
    # Additional development-specific settings
    CORS_ORIGINS = BaseConfig.CORS_ORIGINS + [
        "http://localhost:3000",  # React dev server
        "http://127.0.0.1:3000"
    ]

class TestingConfig(BaseConfig):
    """Testing configuration."""
    
    DEBUG: bool = False
    TESTING: bool = True
    
    # Use a temporary directory for test data
    VENUE_DATA_DIR: str = os.environ.get(
        'TEST_VENUE_DATA_DIR',
        str(Path('/tmp/venue-playlists-test/data'))
    )
    
    # Use same CORS settings as base config for testing
    CORS_ORIGINS: list[str] = BaseConfig.CORS_ORIGINS

class ProductionConfig(BaseConfig):
    """Production configuration."""
    
    DEBUG: bool = False
    TESTING: bool = False
    
    # Stricter security settings
    SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_HTTPONLY: bool = True
    PERMANENT_SESSION_LIFETIME: int = 3600  # 1 hour
    
    # Production CORS settings - should be set via environment
    DEFAULT_ALLOWED_ORIGINS = [
        "https://venue-playlists.vercel.app",  # Primary Vercel domain
        "https://*.venue-playlists.vercel.app",  # All Vercel preview deployments
        "https://venue-playlists-*.vercel.app"   # All Vercel production deployments
    ]
    
    # Use environment ALLOWED_ORIGINS if set, otherwise use defaults
    CORS_ORIGINS: list[str] = (
        os.environ.get('ALLOWED_ORIGINS', '').split(',') if os.environ.get('ALLOWED_ORIGINS')
        else DEFAULT_ALLOWED_ORIGINS
    )
    
    # Production settings that must be overridden
    SECRET_KEY: str = os.environ.get('SECRET_KEY', '')  # Empty string as default, but should be set in production
    LOG_LEVEL: str = 'WARNING'
    
    def __init__(self):
        """Validate production configuration."""
        super().__init__()
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY must be set in production environment")
        if not self.CORS_ORIGINS:
            raise ValueError("CORS_ORIGINS must not be empty in production")

# Configuration dictionary
config: Dict[str, Any] = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config(env: Optional[str] = None) -> Any:
    """Get the configuration class based on environment.
    
    Args:
        env: The environment name. If None, will use FLASK_ENV environment variable
             or fall back to 'default'
             
    Returns:
        The configuration class for the specified environment
    """
    if env is None:
        env = os.environ.get('FLASK_ENV', 'default')
    return config[env] 