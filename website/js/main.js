document.addEventListener('DOMContentLoaded', function() {
    loadVenues();
});

async function loadVenues(retries = 3) {
    try {
        const response = await fetch('/data/sf_venues.json');
        if (!response.ok) {
            if (response.status === 404) {
                console.error('Venue data file not found');
                document.getElementById('venue-grid').innerHTML = 
                    '<div class="error-message">No venue data available</div>';
                return;
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const venues = await response.json();
        
        const venueGrid = document.getElementById('venue-grid');
        venueGrid.innerHTML = ''; // Clear existing content
        
        venues.forEach(venue => {
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
        document.getElementById('venue-grid').innerHTML = `
            <div class="error-message">
                Failed to load venue data: ${error.message}
            </div>
        `;
    }
}

function createVenueCard(venue) {
    const card = document.createElement('div');
    card.className = 'venue-card';
    card.innerHTML = `
        <h2 class="venue-name">${venue.name}</h2>
        <div class="month-sections">
            ${venue.months.map((month, index) => createMonthSection(month, index === 0)).join('')}
        </div>
    `;
    return card;
}

function createMonthSection(month, isFirst = false) {
    const collapsedClass = isFirst ? '' : 'collapsed';
    const arrowDirection = isFirst ? '▼' : '▶';
    
    return `
        <div class="month-section">
            <h3 onclick="togglePlaylist(this)">
                ${formatMonth(month.name)} <span class="arrow">${arrowDirection}</span>
            </h3>
            <div class="playlist-container ${collapsedClass}">
                <iframe 
                    src="https://open.spotify.com/embed/playlist/${getPlaylistId(month.playlist_url)}"
                    width="100%" 
                    height="380" 
                    frameborder="0" 
                    allowtransparency="true" 
                    allow="encrypted-media">
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