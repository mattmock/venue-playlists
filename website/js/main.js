import config from './config.js';

document.addEventListener('DOMContentLoaded', function() {
    loadVenues();
});

function hasValidPlaylistData(venue) {
    return venue.months && 
           venue.months.length > 0;
}

async function loadVenues(retries = 3) {
    try {
        const response = await fetch('/data/sf_venues.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const venuesWithPlaylists = await response.json();
        
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
            acc + venue.months.length, 0);
        loadedIframes = 0; // Reset counter
        
        venuesWithPlaylists.forEach(venue => {
            const card = createVenueCard(venue);
            venueGrid.appendChild(card);
        });
        
    } catch (error) {
        console.log(`Retrying... ${retries} attempts left`);
        if (retries > 0) {
            await new Promise(resolve => setTimeout(resolve, 1000));
            await loadVenues(retries - 1);
        } else {
            console.error('Error loading venues:', error);
            const venueGrid = document.getElementById('venue-grid');
            venueGrid.innerHTML = '<div class="error-message">Failed to load venues. Please try again later.</div>';
        }
    }
}

function createVenueCard(venue) {
    const card = document.createElement('div');
    card.className = 'venue-card';
    
    const title = document.createElement('h2');
    title.className = 'venue-name';
    title.textContent = venue.name;
    card.appendChild(title);
    
    const monthSections = document.createElement('div');
    monthSections.className = 'month-sections';
    
    // Sort months chronologically
    const sortedMonths = venue.months.sort((a, b) => {
        const [aMonth, aYear] = a.name.split('_');
        const [bMonth, bYear] = b.name.split('_');
        
        // Compare years first
        if (aYear !== bYear) {
            return aYear - bYear;
        }
        
        // If years are equal, compare months
        const months = ['january', 'february', 'march', 'april', 'may', 'june',
                       'july', 'august', 'september', 'october', 'november', 'december'];
        return months.indexOf(aMonth.toLowerCase()) - months.indexOf(bMonth.toLowerCase());
    });
    
    sortedMonths.forEach((monthData, index) => {
        const section = createMonthSection(monthData.name, monthData, index === 0);
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
    container.classList.toggle('collapsed');
    const arrow = element.querySelector('.arrow');
    arrow.textContent = container.classList.contains('collapsed') ? '▶' : '▼';
}

function formatMonth(monthStr) {
    const [month, year] = monthStr.split('_');
    return `${month.charAt(0).toUpperCase() + month.slice(1)} ${year}`;
} 