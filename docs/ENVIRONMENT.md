# Environment Configuration

## Development Setup

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Fill in your credentials in `.env` (see below for required values)
3. Start the servers using VS Code tasks:
   - `Start API Server`: http://localhost:8080
   - `Start Frontend Server`: http://localhost:8000
   - Or use `Start All Servers` to launch both

### Required Credentials
See `.env.example` for details and format:
- Spotify API credentials (required for playlist management)
- Flask configuration (defaults work for development)
- Optional path overrides if needed

### Project Structure
```
venue-playlists/
├── data/venue-data/    # Venue data files
├── logs/              # Application logs
├── scripts/           # CLI tools
├── venue_playlists_api/ # API package
└── website/           # Static frontend
```

## Production Setup (DigitalOcean)

### Initial Server Setup
1. Create Ubuntu droplet (512MB RAM minimum)
2. Set up SSH access and basic security
3. Install dependencies: Python 3.12, nginx, certbot

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

## Personal Notes
- Keep a copy of production credentials in Bitwarden
- Document any custom changes or configurations here
- Add deployment/update procedures as they're developed