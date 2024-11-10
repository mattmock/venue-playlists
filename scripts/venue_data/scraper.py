from bs4 import BeautifulSoup
import requests
import re
from . import config
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def fetch_venue_page(venue_key: str) -> str:
    """Fetch raw HTML for a venue's page."""
    if venue_key not in config.VENUES:
        raise ValueError(f"Unknown venue: {venue_key}")
    
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1)
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    url = config.VENUES[venue_key]["url"]
    response = session.get(url, headers=config.HTTP_HEADERS, timeout=30)
    response.raise_for_status()
    return response.content

def clean_calendar_text(html_content: str) -> str:
    """Clean and extract text from HTML content."""
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Remove noise elements
    for script in soup(["script", "style", "footer", "header", "nav"]):
        script.decompose()
    
    # Clean text
    text = soup.get_text(separator=' ')
    return re.sub(r'\s+', ' ', text).strip() 