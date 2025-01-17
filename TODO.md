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
   - User Authentication Features:
     - Analyze user's Spotify listening history for better recommendations
     - Create personalized venue recommendations based on music taste
     - Alert users when similar artists announce shows
     - Track which recommendations led to event attendance

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

## Future Ideas & Concepts
Ideas that need more exploration and brainstorming before moving to concrete features.

- [ ] Spotify Playlist Organization
  - Challenge: Spotify API doesn't support folder management
  - Potential Solutions:
    - Implement consistent naming convention (e.g., "[City] - [Venue] - [Month Year]")
    - Use playlist descriptions for enhanced metadata
    - Focus on website as primary browsing interface
  - Questions to Explore:
    - Impact on user experience for direct Spotify profile browsers
    - Trade-offs between different naming conventions
    - Ways to maintain organization as project scales to more cities

- [ ] Spotify Web UI Automation for Folder Management
  - Challenge: Automate folder creation/management through Spotify's web interface
  - Technical Approach:
    - Use Selenium/Playwright to interact with Spotify Web Player
    - Simulate manual folder creation and playlist organization
  - Major Considerations:
    - High maintenance burden due to UI changes
    - Session handling and authentication complexity
    - Potential rate limiting or detection by Spotify
    - Need for robust error handling and recovery
  - Might be worth exploring as proof of concept, but likely too fragile for production use

- [ ] Integrated Music Discovery & Event Tracking
  - Challenge: Users discover songs they like while browsing playlists in Spotify, but connecting back to the live event is cumbersome
  - Use Case Focus:
    - Quick sampling of venue's upcoming artists
    - Easy way to preview and track interesting shows
    - NOT meant for extended listening sessions
  - Potential Solutions:
    - Integrate Spotify Web Playback SDK for quick previews:
      - 30-second song samples with artist/event context
      - Simple "like/save event" button while previewing
      - Quick skip/next to sample different artists
      - Emphasis on event details over playback controls
    - Add custom playlist descriptions with direct links to event pages
    - Build a lightweight "interested in" tracking system
    - Focus on bridging discovery to ticket purchase/event tracking
  - User Authentication Benefits:
    - Save interesting shows while sampling
    - Quick-add to personal event tracking list
    - Basic preferences for music recommendations
  - Questions to Explore:
    - How to optimize the UI for quick sampling vs extended listening
    - Ways to make event tracking/saving as frictionless as possible
    - Premium subscription requirement impact (Web Playback SDK requires Spotify Premium)
    - Browser compatibility and mobile support considerations
    - User data privacy considerations and GDPR compliance
    - Strategy for users without Premium (fallback features)
    - Balance between feature utility and app simplicity