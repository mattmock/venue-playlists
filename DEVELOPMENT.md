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