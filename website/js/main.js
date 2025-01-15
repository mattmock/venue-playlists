document.addEventListener('DOMContentLoaded', function() {
    loadVenues();
});

function hasValidPlaylistData(venue) {
    return venue.months && 
           venue.months.length > 0 && 
           venue.months.some(month => month.playlist_url);
}

async function loadVenues(retries = 3) {
    try {
        const response = await fetch('data/venues.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const venues = await response.json();
        
        // Get venues object from response
        const venuesData = venues.venues;
        
        // Convert to array and filter
        const venuesWithPlaylists = Object.entries(venuesData)
            .map(([key, venue]) => ({
                id: key,
                ...venue
            }))
            .filter(venue => Object.keys(venue.months).length > 0);
        
        const venueGrid = document.getElementById('venue-grid');
        venueGrid.innerHTML = ''; // Clear existing content
        
        if (venuesWithPlaylists.length === 0) {
            venueGrid.innerHTML = '<div class="error-message">No venues with playlists available</div>';
            return;
        }
        
        // Calculate total number of iframes
        totalIframes = venuesWithPlaylists.reduce((acc, venue) => 
            acc + Object.values(venue.months).length, 0);
        loadedIframes = 0; // Reset counter
        
        venuesWithPlaylists.forEach(venue => {
            const card = createVenueCard(venue);
            venueGrid.appendChild(card);
        });
    } catch (error) {
        if (retries > 0) {
            console.log(`Retrying... ${retries} attempts left`);
            await new Promise(r => setTimeout(r, 1000));
            return loadVenues(retries - 1);
        }
        console.error('Error loading venues:', error);
        document.getElementById('venue-grid').innerHTML = 
            `<div class="error-message">Failed to load venue data: ${error.message}</div>`;
    }
}

function createVenueCard(venue) {
    const card = document.createElement('div');
    card.className = 'venue-card';
    card.innerHTML = `
        <h2 class="venue-name">${venue.name}</h2>
        <p class="venue-description">${venue.description || ''}</p>
        <div class="month-sections">
            ${Object.entries(venue.months)
                .map(([monthKey, monthData], index) => 
                    createMonthSection(monthKey, monthData, index === 0)
                ).join('')}
        </div>
    `;
    return card;
}

let totalIframes = 0;
let loadedIframes = 0;

function handleIframeLoad() {
    loadedIframes++;
    if (loadedIframes === totalIframes) {
        document.getElementById('loading-overlay').classList.add('hidden');
    }
}

function createMonthSection(monthKey, monthData, isFirst = false) {
    const collapsedClass = isFirst ? '' : 'collapsed';
    const arrowDirection = isFirst ? '▼' : '▶';
    
    return `
        <div class="month-section">
            <h3 onclick="togglePlaylist(this)">
                ${formatMonth(monthKey)} <span class="arrow">${arrowDirection}</span>
            </h3>
            <div class="playlist-container ${collapsedClass}">
                <iframe 
                    src="https://open.spotify.com/embed/playlist/${getPlaylistId(monthData.playlist_url)}"
                    height="380" 
                    frameborder="0" 
                    allowtransparency="true" 
                    allow="encrypted-media"
                    onload="handleIframeLoad()">
                </iframe>
            </div>
        </div>
    `;
}

function getPlaylistId(url) {
    return url.split('/').pop();
}

function togglePlaylist(element) {
    const container = element.nextElementSibling;
    const arrow = element.querySelector('.arrow');
    container.classList.toggle('collapsed');
    arrow.textContent = container.classList.contains('collapsed') ? '▶' : '▼';
}

function formatMonth(monthStr) {
    const [month, year] = monthStr.split('_');
    return `${month.charAt(0).toUpperCase() + month.slice(1)} ${year}`;
} 