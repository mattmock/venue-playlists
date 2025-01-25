from . import storage

# HTTP request headers
HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_venues():
    """Load venue configuration."""
    return storage.load_venue_config().get('venues', {})

# Load venues on module import
VENUES = get_venues()
 