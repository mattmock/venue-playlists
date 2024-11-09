from venue_data.main import process_venue
from venue_data.storage import load_venue_config

if __name__ == "__main__":
    try:
        venues = load_venue_config()
        for venue_key in venues.keys():
            output_files = process_venue(venue_key)
            print(f"Processed {venue_key}. Results saved to:")
            for file in output_files:
                print(f"  - {file}")
    except Exception as e:
        print(f"Error processing venues: {e}")