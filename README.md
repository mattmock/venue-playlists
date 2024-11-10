# Venue Playlists

A tool for collecting venue events and generating Spotify playlists.

## Setup

### Prerequisites
- Python 3.8+
- A Spotify Developer account

### Spotify Configuration
1. Create a Spotify Developer application at https://developer.spotify.com/dashboard
2. Note your Client ID and Client Secret
3. Add a redirect URI (e.g., `http://localhost:8888/callback`)
4. Create a `.env` file in the project root with the following:

```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=your_redirect_uri
```

## Project Structure

```
.
├── data/
│   └── venue-data/
│       └── {city}/
│           ├── venues.yaml
│           └── {venue}/
│               ├── artists_{month}.yaml
│               └── playlist_{month}.yaml
└── scripts/
    ├── collect_events.py
    ├── generate_playlists.py
    ├── venue_data/
    └── playlist_data/
```

## Code References

Key components of the codebase:

### Event Collection

Location: `scripts/venue_data/main.py` (lines 18-42)

### Playlist Generation

Location: `scripts/playlist_data/generator.py` (lines 49-77)

### Configuration

Location: `scripts/playlist_data/config.py` (lines 7-18)