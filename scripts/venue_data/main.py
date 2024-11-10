from . import scraper, text_utils, storage
from .extractor import ArtistExtractor
from typing import List
from datetime import datetime

def process_venue(venue_key: str, output_dir: str = "data/venue-data/sf") -> List[str]:
    """Process a venue and extract artists for the next 3 months."""
    try:
        # Fetch and clean HTML
        html_content: bytes = scraper.fetch_venue_page(venue_key)
        cleaned_text: str = scraper.clean_calendar_text(html_content)
        
        # Split into chunks if needed
        text_chunks = text_utils.chunk_message(cleaned_text)
        
        # Extract artists with dates
        extractor = ArtistExtractor()
        artist_events = extractor.process_chunks(text_chunks)
        
        # Save results for each month
        output_files = []
        for month in text_utils.get_next_months():
            filename = storage.save_artists_to_file(venue_key, artist_events, month, output_dir)
            output_files.append(filename)
            
        return output_files
        
    except Exception as e:
        print(f"Error processing venue {venue_key}: {e}")
        raise

if __name__ == "__main__":
    output_files = process_venue("independent")
    print(f"Results saved to: {output_files}") 