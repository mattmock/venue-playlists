# Environment Configuration

## Development Environment

### Required Environment Variables
```bash
# API Configuration
FLASK_APP=venue_playlists_api
FLASK_ENV=development
FLASK_DEBUG=1

# Spotify API (required for playlist management)
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REFRESH_TOKEN=your_refresh_token

# Optional Overrides
VENUE_DATA_DIR=/path/to/data  # Defaults to PROJECT_ROOT/data/venue-data
VENUE_PLAYLISTS_ROOT=/path/to/root  # Auto-detected if not set
```

### Local Development Setup
- API Server: http://localhost:8080
- Frontend Server: http://localhost:8000
- VS Code tasks handle server management:
  - `Start API Server`: Runs Flask development server
  - `Start Frontend Server`: Serves static files
  - `Start All Servers`: Launches both servers
  - `Restart Servers`: Full restart of both servers

### Directory Structure
```
venue-playlists/
├── data/
│   └── venue-data/      # Venue data files
│       └── sf/          # City-specific data
├── logs/                # Application logs
├── scripts/            # CLI tools
├── venue_playlists_api/ # API package
└── website/            # Static frontend
```

### Development Tools
- Python 3.12+
- Flask 3.0+
- VS Code with Python extension
- Chrome/Firefox for testing

## Production Environment

### Required Environment Variables
```bash
# API Configuration
FLASK_APP=venue_playlists_api
FLASK_ENV=production
SECRET_KEY=your_secure_key  # Required in production

# CORS Configuration
ALLOWED_ORIGINS=https://your-domain.com,https://api.your-domain.com

# Spotify API
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REFRESH_TOKEN=your_refresh_token
```

### Security Requirements
- HTTPS required for all endpoints
- Secure cookie settings enabled
- Rate limiting configured
- CORS restricted to specific domains

### Logging Configuration
- Application logs: `/var/log/venue-playlists/`
  - API access logs
  - Error logs
  - Script execution logs
- Log rotation enabled
- Structured logging format

### Resource Requirements
- CPU: 1 core minimum
- RAM: 2GB minimum
- Storage: 20GB minimum
- Network: Standard DO bandwidth

### Backup Requirements
- Daily venue data backups
- Weekly system backups
- Spotify credentials backup
- Configuration backup 