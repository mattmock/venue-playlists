# Development Guide

> For additional documentation, please see the [project wiki](../vp-wiki).

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **APIs**: Spotify Web API, OpenAI API
- **Infrastructure**: 
  - Vercel (frontend hosting)
  - DigitalOcean (API & automation)
  - Nginx (reverse proxy)
- **Data**: YAML, JSON

## Setup

### Prerequisites
- Python 3.12 or higher
- Poetry (Python package manager)
- A Spotify Developer account
- An OpenAI API key
- Chrome/Chromium (for Selenium)

### First-Time Setup
1. Install Poetry:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Clone and set up the project:
   ```bash
   git clone git@github.com:yourusername/venue-playlists.git
   cd venue-playlists
   poetry install
   ```

3. Create and configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Activate the virtual environment:
   ```bash
   poetry shell
   ```

### Configuration
Required settings in `.env`:
```env
# Required credentials
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
OPENAI_API_KEY=your_openai_api_key

# Flask configuration (development defaults)
FLASK_ENV=development

# Development settings
PYTHONPATH=.
LOGLEVEL=DEBUG
SAVE_ALL_SCREENSHOTS=true
```

### Development Tools
The project uses several development tools, all managed through Poetry:

- **Black**: Code formatting
  ```bash
  poetry run black .
  ```

- **isort**: Import sorting
  ```bash
  poetry run isort .
  ```

- **Flake8**: Code linting
  ```bash
  poetry run flake8
  ```

- **MyPy**: Type checking
  ```bash
  poetry run mypy .
  ```

- **pytest**: Testing with coverage
  ```bash
  poetry run pytest
  ```

### VS Code Integration
The project includes VS Code settings for:
- Python interpreter selection
- Test discovery and running
- Code formatting on save
- Import organization
- Environment variable loading

To use these features, install the Python extension for VS Code and reload the window after opening the project.

### Project Structure
```
venue-playlists/
├── data/
│   ├── examples/       # Example venue data files
│   └── venue-data/    # Active venue data
├── logs/              # Application logs
├── data_processing/   # Data processing modules
├── venue_playlists_api/ # API package
└── website/           # Static frontend
```

## Data Structure

Example venue configuration (see `data/examples/sf/venues.yaml`):
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

## Production Deployment

### Server Setup (DigitalOcean)
1. Create Ubuntu droplet (512MB RAM minimum)
2. Set up SSH access and basic security
3. Install dependencies: Python 3.12, nginx, certbot
4. Configure automated updates (see Infrastructure Runbook in wiki)

### Environment Setup
1. Store production credentials in `/etc/venue-playlists/.env`:
   ```bash
   sudo mkdir /etc/venue-playlists
   sudo nano /etc/venue-playlists/.env
   sudo chmod 640 /etc/venue-playlists/.env
   ```

2. Required production settings:
   - `FLASK_ENV=production`
   - `SECRET_KEY` (generate a secure one)
   - `ALLOWED_ORIGINS` (your domain)
   - All Spotify API credentials

### Backup Strategy
Keep secure copies of:
- Production `.env` file
- Nginx configuration
- SSL certificates
- Venue data (in `/opt/venue-playlists/data`)

### Maintenance Notes
- Logs are in `/var/log/venue-playlists/`
- Use `systemctl restart venue-playlists` to restart the service
- Certbot auto-renews SSL certificates
- Keep a copy of production credentials in Bitwarden
- See Infrastructure Runbook in wiki for detailed procedures

### Website Deployment
1. Generate data locally:
   ```bash
   python scripts/build_website_data.py
   ```

2. Deploy to Vercel:
   ```bash
   # Create preview deployment (for testing)
   vercel deploy website/
   # Select "venue-playlists" when prompted
   # Preview URL will look like: venue-playlists-{hash}.vercel.app
   
   # Or deploy to production when ready
   vercel deploy website/ --prod
   # Production URL: venue-playlists.vercel.app
   ```

For detailed deployment procedures and troubleshooting, see the Infrastructure Runbook in the project wiki. 