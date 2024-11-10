# Venue Playlists

A tool for collecting venue events and generating Spotify playlists.

## Setup

### Prerequisites
- Python 3.8+
- A Spotify Developer account
- An OpenAI API key

### Configuration
Create a `.env` file:
```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
OPENAI_API_KEY=your_openai_api_key
```

### First-Time Setup
Run `python scripts/collect_events.py` to authenticate with Spotify. This will:
- Open a browser window for authorization
- Save the refresh token to your `.env` file

## Usage

### Collecting Events
```bash
python scripts/collect_events.py
```

### Generating Playlists
```bash
python scripts/generate_playlists.py
```

## Data Structure

Each venue needs a config in `data/venue-data/{city}/venues.yaml`:
```yaml
venue_key:
  name: "Venue Name"
  url: "https://venue-calendar-url.com"
  scraper: "scraper_type"
```

The tool generates:
1. Monthly artist listings (`artists_{month}.yaml`)
2. Playlist metadata (`playlist_{month}.yaml`)