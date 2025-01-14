# Venue Playlists

A tool for collecting venue events and generating Spotify playlists.

## Setup

### Prerequisites
- Python 3.8+
- A Spotify Developer account
- An OpenAI API key
- Chrome/Chromium (for Selenium)

### Configuration
Create a `.env` file:
```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
OPENAI_API_KEY=your_openai_api_key

# Scraper settings
PYTHONPATH=.
LOGLEVEL=DEBUG
SAVE_ALL_SCREENSHOTS=true
```

### First-Time Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run initial setup:
```bash
python scripts/collect_events.py
```
This will:
- Open a browser window for authorization
- Save the refresh token to your `.env` file

## Usage

### Collecting Events
# Collect all venues
```bash
python scripts/collect_events.py
```

# Force update specific venue
```bash
python scripts/collect_events.py --force the-independent
```

# Force update all venues
```bash
python scripts/collect_events.py --force-all
```

### Generating Playlists
```bash
python scripts/generate_playlists.py
```

## Testing
```bash
# Run all tests
pytest scripts/tests/ -v

# Run specific test file
pytest scripts/tests/test_venue_data.py -v

# Run specific test
pytest scripts/tests/test_venue_data.py::test_venue_processing -v
```

## Data Structure

Each venue needs a config in `data/venue-data/{city}/venues.yaml`:
```yaml
venues:
  venue_key:
    name: "Venue Name"
    description: "Venue description"
    scrapers:
      bandisintown:
        url: "https://www.bandsintown.com/v/venue-id"
        priority: 1
      website:  # future support
        url: "https://venue-website.com/calendar"
        priority: 2
```

The tool generates:
1. Monthly artist listings (`artists_{month}.yaml`)
2. Playlist metadata (`playlist_{month}.yaml`)