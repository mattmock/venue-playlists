# Droplet Migration Plan

## Overview
This document outlines the step-by-step plan for migrating the venue-playlists application from local development to a DigitalOcean droplet.

## Pre-Migration Tasks
- [x] Script Adaptations
  - [x] Update collect_events.py to use API's venue data structure
    - Using load_venue_config for API-compatible venue loading
    - Added proper logging with file and console output
    - Added test mode with --test-venues option
    - Fixed type hints and error handling
  - [x] Update generate_playlists.py to align with API expectations
    - Added proper logging with file and console output
    - Added test mode options (--test-venues, --months)
    - Added auto-cleanup of test playlists with --preserve-test flag
    - Fixed type hints and error handling
  - [x] Remove build_website_data.py (replaced by API)
  - [x] Update update_all.py to remove website data build step
    - Added proper logging with file output
    - Switched to load_venue_config instead of static VENUES
    - Improved error handling and reporting
  - [x] Add proper logging to all scripts
    - Added to generate_playlists.py (file + console)
    - Added to update_all.py (file + console)
    - Remaining: collect_events.py
  - [x] Test scripts with local API
    - Successfully tested generate_playlists.py with test mode
    - Successfully tested collect_events.py with test venues
    - Successfully tested update_all.py with new structure
    - All scripts working with API via VS Code tasks
  - [x] Document new script behaviors and requirements
    - Updated DEVELOPMENT.md with comprehensive test mode documentation
    - Added details for all new command options
- [ ] Local Testing
  - [x] Run full end-to-end test locally
    - Successfully tested complete flow with The Independent
    - Collect events → Generate playlist → Cleanup
    - All components working through API
  - [x] Verify all API endpoints with production configuration
    - Venue data endpoints working
    - Playlist management endpoints working
    - Error handling verified
  - [x] Test CORS with production domain
    - Frontend (8000) and API (8080) communicating
    - CORS headers properly configured
  - [x] Document any environment-specific configurations
    - Created ENVIRONMENT.md with comprehensive documentation
    - Documented development and production requirements
    - Added directory structure and tool requirements
    - Specified all required environment variables

## Prerequisites
- [ ] DigitalOcean account
- [ ] Domain name
- [ ] SSH key pair for secure access
- [ ] Basic firewall rules planned
- [x] Production environment variables documented
  - See ENVIRONMENT.md for complete list
- [x] Backup strategy defined
  - Daily venue data backups
  - Weekly system backups
  - Credentials and config backups
- [x] Resource requirements estimated
  - 512MB RAM (lightweight API and scripts)
  - 1 CPU core
  - 20GB storage
  - Standard network bandwidth

## Migration Steps

### 1. Droplet Setup
- [ ] Create Ubuntu 22.04 LTS droplet (2GB RAM minimum recommended)
- [ ] Configure SSH access with key authentication only
- [ ] Update system packages
- [ ] Install required dependencies:
  - Python 3.12
  - pip
  - nginx
  - certbot
  - git
  - ufw (firewall)
- [ ] Configure basic firewall (SSH, HTTP, HTTPS)
- [ ] Set up fail2ban for SSH protection

### 2. Application Deployment
- [ ] Clone repository
- [ ] Set up Python virtual environment
- [ ] Install application dependencies
- [ ] Install and configure Gunicorn
  - Set worker count based on CPU cores
  - Configure timeout settings
  - Set up error handling
- [ ] Create systemd service for API
  - Configure automatic restarts
  - Set environment variables
- [ ] Configure logging
  - Application logs in /var/log/venue-playlists/
  - Access logs
  - Error logs
  - Set up log rotation

### 3. Web Server Configuration
- [ ] Configure nginx as reverse proxy
  - Set up proper buffering
  - Configure gzip compression
  - Set up request size limits
- [ ] Set up SSL with Let's Encrypt
  - Configure auto-renewal
  - Set up strong SSL parameters
- [ ] Configure proper headers (CORS, security)
  - Set CORS for production domain
  - Add security headers (HSTS, XSS protection, etc.)
- [ ] Set up static file serving for frontend
  - Configure caching headers
  - Set up compression

### 4. Scripts Setup
- [ ] Create dedicated user for running scripts
- [ ] Set up cron jobs for automated updates
  - Configure proper timing
  - Add error notifications
- [ ] Configure script logging
  - Separate log file for each script
  - Rotation policy
- [ ] Update script configurations to use production API endpoint
- [ ] Set up error notification system

### 5. Monitoring
- [ ] Set up basic system monitoring
  - CPU usage
  - Memory usage
  - Disk space
  - Network traffic
- [ ] Configure log rotation
  - Set retention periods
  - Configure compression
- [ ] Set up automated backups
  - Daily venue data backups
  - Weekly system backups
- [ ] Implement basic health checks
  - API endpoint monitoring
  - System resource monitoring
  - Certificate expiration monitoring

### 6. Testing
- [ ] Verify API functionality
  - Run API tests against production
  - Verify rate limiting
- [ ] Test frontend integration
  - Check CORS in production
  - Verify loading states
- [ ] Validate script execution
  - Test cron jobs
  - Verify logging
- [ ] Check logging and monitoring
- [ ] Load testing (if needed)
  - Simulate concurrent users
  - Monitor resource usage

### 7. DNS Configuration
- [ ] Configure A records
- [ ] Set up www subdomain
- [ ] Configure HTTPS redirects
- [ ] Set appropriate TTL values
- [ ] Document DNS settings

## Rollback Plan
1. Keep local development environment intact
2. Maintain backup of all configuration files
3. Document all custom configurations
4. Keep snapshot of initial droplet setup
5. Maintain DNS records for quick switching
6. Document rollback procedures and triggers

## Security Considerations
- Firewall configuration
  - Limit SSH access
  - Rate limit API endpoints
- Regular security updates
  - Enable unattended-upgrades
  - Schedule maintenance windows
- Secure key storage
  - Use environment variables
  - Implement secrets management
- Rate limiting
  - API endpoints
  - Failed login attempts
- Regular backup strategy
  - Automated backups
  - Off-site storage
- Monitor security logs

## Post-Migration Tasks
- [ ] Update documentation
  - Update README
  - Document deployment process
  - Update development setup guide
- [ ] Set up monitoring alerts
  - Disk space warnings
  - Error rate alerts
  - Certificate expiration
- [ ] Create maintenance procedures
  - Backup verification
  - Log rotation
  - Security updates
- [ ] Document recovery procedures
  - Service restoration
  - Data recovery
  - DNS fallback 