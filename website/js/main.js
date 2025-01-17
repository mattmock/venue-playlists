import config from './config.js';

document.addEventListener('DOMContentLoaded', function() {
    loadVenues();
});

function hasValidPlaylistData(venue) {
    return venue.months && 
           Object.keys(venue.months).length > 0;
}

async function loadVenues(retries = 3) {
    try {
        const response = await fetch(`${config.apiUrl}/venues`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        
        // Get venues object from response
        const venuesData = data.venues;
        
        // Convert to array and filter
        const venuesWithPlaylists = Object.entries(venuesData)
            .map(([key, venue]) => ({
                id: key,
                ...venue
            }))
            .filter(hasValidPlaylistData);
        
        const venueGrid = document.getElementById('venue-grid');
        venueGrid.innerHTML = ''; // Clear existing content
        
        if (venuesWithPlaylists.length === 0) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.textContent = 'No venues with playlists available';
            venueGrid.appendChild(errorDiv);
            return;
        }
        
        // Calculate total number of iframes
        totalIframes = venuesWithPlaylists.reduce((acc, venue) => 
            acc + Object.keys(venue.months).length, 0);
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
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = `Failed to load venue data: ${error.message}`;
        document.getElementById('venue-grid').innerHTML = '';
        document.getElementById('venue-grid').appendChild(errorDiv);
    }
}

function createVenueCard(venue) {
    const card = document.createElement('div');
    card.className = 'venue-card';
    
    const title = document.createElement('h2');
    title.className = 'venue-name';
    title.textContent = venue.name;
    card.appendChild(title);
    
    const description = document.createElement('p');
    description.className = 'venue-description';
    description.textContent = venue.description || '';
    card.appendChild(description);
    
    const monthSections = document.createElement('div');
    monthSections.className = 'month-sections';
    
    // Sort months chronologically
    const sortedMonths = Object.entries(venue.months).sort(([aKey], [bKey]) => {
        const [aMonth, aYear] = aKey.split('_');
        const [bMonth, bYear] = bKey.split('_');
        
        // Compare years first
        if (aYear !== bYear) {
            return aYear - bYear;
        }
        
        // If years are equal, compare months
        const months = ['january', 'february', 'march', 'april', 'may', 'june',
                       'july', 'august', 'september', 'october', 'november', 'december'];
        return months.indexOf(aMonth.toLowerCase()) - months.indexOf(bMonth.toLowerCase());
    });
    
    sortedMonths.forEach(([monthKey, monthData], index) => {
        const section = createMonthSection(monthKey, monthData, index === 0);
        monthSections.appendChild(section);
    });
    
    card.appendChild(monthSections);
    return card;
}

let totalIframes = 0;
let loadedIframes = 0;

// Make handleIframeLoad globally accessible
window.handleIframeLoad = function() {
    loadedIframes++;
    console.log(`Iframe loaded: ${loadedIframes}/${totalIframes}`);
    if (loadedIframes === totalIframes) {
        const overlay = document.getElementById('loading-overlay');
        overlay.classList.add('hidden');
        console.log('All iframes loaded, hiding overlay');
    }
}

function createMonthSection(monthKey, monthData, isFirst = false) {
    const collapsedClass = isFirst ? '' : 'collapsed';
    const arrowDirection = isFirst ? '▼' : '▶';
    
    const section = document.createElement('div');
    section.className = 'month-section';
    
    const header = document.createElement('h3');
    header.onclick = function() { togglePlaylist(this); };
    
    const monthText = document.createTextNode(formatMonth(monthKey) + ' ');
    header.appendChild(monthText);
    
    const arrow = document.createElement('span');
    arrow.className = 'arrow';
    arrow.textContent = arrowDirection;
    header.appendChild(arrow);
    
    section.appendChild(header);
    
    const container = document.createElement('div');
    container.className = `playlist-container ${collapsedClass}`;
    
    const iframe = document.createElement('iframe');
    iframe.src = `https://open.spotify.com/embed/playlist/${getPlaylistId(monthData.playlist_url)}`;
    iframe.height = "380";
    iframe.frameBorder = "0";
    iframe.allowTransparency = true;
    iframe.allow = "encrypted-media";
    iframe.addEventListener('load', window.handleIframeLoad);
    
    container.appendChild(iframe);
    section.appendChild(container);
    
    return section;
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