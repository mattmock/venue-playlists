# Project TODOs

## High Priority
- [X] Set up Vercel deployment for frontend
- [X] Move away from dependence on Open AI API - use only as a fallback
- [ ] Migrate to API-based Architecture
    - Phase 1: Basic API Setup (Massive Win)
      - Set up FastAPI/Flask server
      - Serve existing YAML data through API
      - Add basic error handling
      - Deploy to DigitalOcean
    - Backend Service Setup:
      - Set up API server on DigitalOcean droplet
      - Configure Nginx
        - Route requests to prod/dev APIs
        - Set up SSL certificates
        - Configure security headers
      - Create venues/playlists/events endpoints
      - Move playlist generation logic to backend
      - Set up PostgreSQL database
    - Phase 2: Environment Setup (Huge Win)
      - Set up development environment
      - Configure staging environment
      - Document environment setup
      - Add environment variables
    - Frontend Updates:
      - Add environment-based API URLs
      - Update fetch logic to use API
      - Improve error handling
      - Enable Vercel auto-deploys
    - Development Workflow:
      - Configure local development environment
      - Set up staging/development API endpoints
      - Document new development process
    - Deployment Pipeline:
      - Set up GitHub Actions for API deployment
      - Configure staging/production environments
      - Add automated testing
- [ ] Set up DigitalOcean VPS for automated playlist generation

## Infrastructure Setup
1. Create Dedicated Spotify Account
   - Set up new account "SF Venue Playlists"
   - Update Spotify Developer settings
   - Update environment variables
   - Test playlist generation with new account

2. Digital Ocean Deployment
   - Migrate project to existing droplet
   - Set up Python virtual environment
   - Copy configuration files
   - Set up environment variables
   - Test playlist generation on server
   - Document deployment process

3. Automation & Monitoring
   - Set up cron jobs for monthly updates
   - Add health checks for scrapers
   - Monitor BandsInTown site structure
   - Set up Discord alerts for:
     - Scraper failures
     - Site structure changes
     - Playlist generation issues

4. Simple Deployment Automation
   - Set up GitHub action for Vercel preview deployments
   - Auto-deploy develop branch to preview URL
   - Keep manual production deployments for safety

## Features
- [ ] Support for additional cities beyond SF
- [ ] Automated City Expansion:
   - Venue Discovery:
     - Semi-automated venue discovery:
       - Generate initial venue list from Google Places/Reviews
       - Simple admin UI to review/edit venues
       - Quick "approve/reject" interface
       - Bulk venue approval for obvious matches
   - Venue Data Collection:
     - Assisted URL matching:
       - Suggest BandsInTown/Songkick URLs
       - Show side-by-side venue comparison
       - "One-click" config generation after approval
   - Quality Control:
     - Confidence scoring for venue matches
     - Manual review interface for low confidence matches
     - Automated venue data validation
- [ ] Add venue filtering by music genre
- [ ] Implement playlist history tracking
- [ ] Smart Artist Discovery:
   - Highlight lesser-known artists similar to user's favorites
   - Show "If you like X, check out Y playing at Z venue"
   - Focus on artists with <100k monthly listeners
   - Compare artist genres with user's top genres
   - Add "Hidden Gems" section for each venue
   - Show Spotify popularity score comparison

## Feature Enhancements
1. Scraper Resilience
   - Add Songkick as backup scraper
   - Improve error handling
   - Add scraper version tracking
   - Add structure change detection

2. Platform Expansion
   - Add YouTube Music support
   - Add Apple Music support
   - Unify playlist creation interface
   - Add platform-specific error handling

## Improvements
- [ ] Add logging for all script executions
- [ ] Add error handling for failed Spotify API requests
- [ ] Implement rate limiting for OpenAI API calls
- [ ] Add tests for venue data scraping
- [ ] Optimize playlist generation performance
- [ ] Enhance mobile responsiveness
- [ ] Add loading states for playlist updates

## Documentation
- Add server setup guide
- Document monthly process
- Add monitoring documentation
- Add troubleshooting guide
- [ ] Document scraper configuration
- [ ] Add API documentation
- [ ] Include deployment instructions