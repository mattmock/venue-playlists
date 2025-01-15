# Development Guide

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

### Test Playlists
When developing or testing, use test mode to avoid cluttering your Spotify:

```bash
# Create playlists in test mode
python scripts/generate_playlists.py --test-mode
```

### Cleaning Up Test Playlists
```bash
# Clean up all test playlists older than 24 hours
python scripts/venue_data/playlist_cleanup.py

# Clean up specific playlist
python scripts/venue_data/playlist_cleanup.py --playlist-id abc123

# Clean up test playlists older than 2 hours
python scripts/venue_data/playlist_cleanup.py --hours 2
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