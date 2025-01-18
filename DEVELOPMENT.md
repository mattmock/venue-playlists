# Development Guide

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

## Testing

### Running Tests
```bash
# Run all tests
pytest scripts/tests/ -v

# Run specific test file
pytest scripts/tests/test_venue_data.py -v

# Run specific test
pytest scripts/tests/test_venue_data.py::test_venue_processing -v
```

## Playlist Management

### Test Mode
When developing or testing, use test mode to avoid cluttering your Spotify:

```bash
# Basic test mode (playlists are auto-cleaned after creation)
python scripts/generate_playlists.py --test-mode

# Test with specific venues
python scripts/generate_playlists.py --test-mode --test-venues the-independent the-fillmore

# Test with limited months
python scripts/generate_playlists.py --test-mode --test-venues the-independent --months 1

# Force update even if playlist exists
python scripts/generate_playlists.py --test-mode --test-venues the-independent --months 1 --force

# Keep test playlists (don't auto-clean)
python scripts/generate_playlists.py --test-mode --test-venues the-independent --preserve-test
```

Test mode features:
- Adds "[TEST] " prefix to playlist names
- Includes creation timestamp in description
- Auto-cleans playlists after creation (unless --preserve-test is used)
- Can be combined with --test-venues and --months for targeted testing

### Cleaning Up Test Playlists
```bash
# Clean up specific playlist
python scripts/venue_data/playlist_cleanup.py --playlist-id abc123
```

## Development Tips
1. Use `LOGLEVEL=DEBUG` for more detailed logging
2. Use `SAVE_ALL_SCREENSHOTS=true` when debugging scraper issues
3. Check `logs/screenshots` for scraper debugging info

## Local Development

### Running the Full Stack
```bash
# 1. Generate playlists (use --test-mode for testing)
python scripts/generate_playlists.py

# 2. Build website data
python scripts/build_website_data.py

# This creates website/data/venues.json (not tracked in git)

# 3. Serve website locally
cd website
python -m http.server 8000
```

Visit http://localhost:8000 to see the site.

### Cleanup
```bash
# Clean up test playlists after development
python scripts/venue_data/playlist_cleanup.py

# Or clean up specific playlist
python scripts/venue_data/playlist_cleanup.py --playlist-id abc123
```

## Deployment

### Deployment Process
1. Generate data locally:
   ```bash
   python scripts/build_website_data.py
   ```

2. Copy generated data to Vercel:
   ```bash
   # Create preview deployment (for testing)
   vercel deploy website/
   # Select "venue-playlists" when prompted
   # Preview URL will look like: venue-playlists-{hash}.vercel.app
   
   # Or deploy to production when ready
   vercel deploy website/ --prod
   # Production URL: venue-playlists.vercel.app
   ``` 