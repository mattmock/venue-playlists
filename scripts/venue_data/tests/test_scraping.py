from venue_data import process_venue, load_venue_config
from venue_data.scrapers import ScraperFactory
from venue_data.models import ArtistEvent

def test_venue_scraping():
    """Test the complete venue scraping process."""
    print("\n1. Testing venue configuration loading...")
    venues = load_venue_config()
    print(f"Found {len(venues)} venues in config")
    
    print("\n2. Testing venue processing...")
    venue_key = "the-independent"
    print(f"Processing {venue_key}...")
    
    # Force update to ensure we get fresh data
    output_files = process_venue(venue_key, force=True)
    
    print("\n3. Results:")
    if output_files:
        print(f"Successfully created {len(output_files)} files:")
        for file in output_files:
            print(f"- {file}")
    else:
        print("No files were created - check for errors above")

if __name__ == "__main__":
    test_venue_scraping()
