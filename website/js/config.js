// Environment-specific configuration
const config = {
    development: {
        apiUrl: 'http://localhost:8080'
    },
    production: {
        apiUrl: 'https://api.venue-playlists.com' // We'll update this when we have the domain
    }
};

// Use development by default, override with production if on actual domain
const isProduction = window.location.hostname !== 'localhost';
const currentConfig = isProduction ? config.production : config.development;

export default currentConfig; 