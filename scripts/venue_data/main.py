from . import scraper, text_utils, storage
from .extractor import ArtistExtractor
from typing import List
from datetime import datetime

def process_venue(venue_key: str, output_dir: str = "data/venue-data/sf", force: bool = False) -> List[str]:
    """Process a venue and extract artists for the next 3 months."""
    try:
        output_files = []
        months = text_utils.get_next_months()
        
        # Skip update check if force is True
        if not force:
            needs_processing = False
            for month in months:
                if storage.needs_update(venue_key, month, output_dir):
                    needs_processing = True
                    break
                    
            if not needs_processing:
                print(f"Skipping {venue_key} - data is up to date")
                return []
            
        # Fetch and process venue data
        html_content: bytes = scraper.fetch_venue_page(venue_key)
        cleaned_text: str = scraper.clean_calendar_text(html_content)
        text_chunks = text_utils.chunk_message(cleaned_text)
        
        # Extract artists with dates
        extractor = ArtistExtractor()
        artist_events = extractor.process_chunks(text_chunks)
        
        # Save results for each month
        for month in months:
            month_name = month.split('_')[0].title()
            month_artists = [ae for ae in artist_events 
                           if ae.date.strftime('%B').lower() == month.split('_')[0]]
            
            if month_artists:  # Only save if we have artists for this month
                filename = storage.save_artists_to_file(venue_key, month_artists, month, output_dir)
                output_files.append(filename)
            else:
                print(f"No artists found for {venue_key} in {month}")
        
        return output_files
        
    except Exception as e:
        print(f"Error processing venue {venue_key}: {e}")
        return []

if __name__ == "__main__":
    output_files = process_venue("independent")
    print(f"Results saved to: {output_files}")