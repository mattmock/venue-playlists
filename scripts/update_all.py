from collect_events import process_city
from generate_playlists import process_city_playlists
from build_website_data import build_venue_data

def update_all(city: str = "sf"):
    # 1. Collect new events
    process_city(city)
    
    # 2. Generate playlists
    process_city_playlists(city)
    
    # 3. Build website data
    build_venue_data(city)

if __name__ == "__main__":
    update_all() 