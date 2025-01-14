import requests
from bs4 import BeautifulSoup

def fetch_venue_page(url: str) -> str:
    """Fetch venue page HTML."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers)
    return response.text

def clean_calendar_text(html: str) -> str:
    """Extract and clean calendar text from HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    # Remove script and style elements
    for element in soup(['script', 'style']):
        element.decompose()
    return soup.get_text() 