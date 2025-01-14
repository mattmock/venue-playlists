import requests
from datetime import datetime, timedelta
from ..bandisintown import BandsinTownScraper
import sys
import logging

# Configure logging
logging.basicConfig(
    filename='bandisintown_scraper_test.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_scraper(venue_url: str):
    """Test the Bandisintown scraper with a specific venue URL."""
    
    # Set up date range (example: current month + next month)
    start_date = datetime.now().replace(day=1)  # First day of current month
    end_date = start_date + timedelta(days=60)  # Roughly two months
    
    logging.info(f"Testing Bandisintown scraper:")
    logging.info(f"URL: {venue_url}")
    logging.info(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    logging.info("-" * 50)
    
    try:
        # Fetch the page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(venue_url, headers=headers)
        response.raise_for_status()
        
        # Parse events
        scraper = BandsinTownScraper()
        events = scraper.extract_events(response.content, start_date, end_date)
        
        # Display results
        logging.info(f"Found {len(events)} events:")
        for event in sorted(events, key=lambda x: x.date):
            logging.info(f"{event.date.strftime('%Y-%m-%d')}: {event.name}")
            
    except Exception as e:
        logging.error(f"Error: {str(e)}")

if __name__ == "__main__":
    # Default test URL or accept from command line
    test_url = "https://www.bandsintown.com/v/10001466-the-independent"
    if len(sys.argv) > 1:
        test_url = sys.argv[1]
    
    test_scraper(test_url) 