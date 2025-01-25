#!/bin/bash

# Check the status of the venue-playlists service
service_status=$(systemctl status venue-playlists)
echo "Service Status:\n$service_status" > server_status.log

# Check the Nginx configuration
nginx_config=$(cat /etc/nginx/sites-available/venue-playlists.conf)
echo "\nNginx Configuration:\n$nginx_config" >> server_status.log

# Test the /api/venues endpoint
api_response=$(curl -I http://127.0.0.1:8080/api/venues)
echo "\nAPI Response for /api/venues:\n$api_response" >> server_status.log

# Log file location
echo "\nLog file generated at: $(pwd)/server_status.log" 