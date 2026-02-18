// Map View JavaScript
let mainMap;
let markers = [];
let markerCluster;

// Initialize map
function initMainMap() {
    // Default to India (Jharkhand)
    const defaultLocation = [23.6102, 85.2799];
    
    mainMap = L.map('mainMap').setView(defaultLocation, 7);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(mainMap);
    
    // Initialize marker cluster group
    markerCluster = L.markerClusterGroup({
        maxClusterRadius: 50,
        spiderfyOnMaxZoom: true,
        showCoverageOnHover: false
    });
    
    // Load complaints
    loadComplaints();
}

// Get marker color based on priority
function getMarkerColor(priority) {
    const colors = {
        'Critical': '#ef4444',
        'High': '#f59e0b',
        'Medium': '#06b6d4',
        'Low': '#64748b'
    };
    return colors[priority] || '#64748b';
}

// Create custom icon
function createCustomIcon(priority) {
    const color = getMarkerColor(priority);
    
    return L.divIcon({
        className: 'custom-marker',
        html: `<div style="
            background-color: ${color};
            width: 30px;
            height: 30px;
            border-radius: 50% 50% 50% 0;
            transform: rotate(-45deg);
            border: 3px solid white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        "></div>`,
        iconSize: [30, 30],
        iconAnchor: [15, 30],
        popupAnchor: [0, -30]
    });
}

// Load complaints on map
function loadComplaints() {
    if (!complaintsData || complaintsData.length === 0) {
        console.log('No complaints to display');
        return;
    }
    
    let pendingCount = 0;
    let progressCount = 0;
    let resolvedCount = 0;
    
    complaintsData.forEach(complaint => {
        if (complaint.latitude && complaint.longitude) {
            const icon = createCustomIcon(complaint.priority);
            
            const marker = L.marker([complaint.latitude, complaint.longitude], {
                icon: icon
            });
            
            // Create popup content
            const popupContent = `
                <div style="min-width: 250px;">
                    <h4 style="margin: 0 0 10px 0; color: #1e293b;">
                        #${complaint.id} - ${complaint.category}
                    </h4>
                    <p style="margin: 5px 0;">
                        <strong>Priority:</strong> 
                        <span style="
                            background: ${getMarkerColor(complaint.priority)};
                            color: white;
                            padding: 2px 8px;
                            border-radius: 12px;
                            font-size: 0.85rem;
                        ">${complaint.priority}</span>
                    </p>
                    <p style="margin: 5px 0;">
                        <strong>Status:</strong> ${complaint.status}
                    </p>
                    <p style="margin: 5px 0;">
                        <strong>Department:</strong> ${complaint.department}
                    </p>
                    <p style="margin: 10px 0; font-size: 0.9rem;">
                        ${complaint.description.substring(0, 100)}${complaint.description.length > 100 ? '...' : ''}
                    </p>
                    ${complaint.image_url ? `
                        <img src="${complaint.image_url}" 
                             style="width: 100%; border-radius: 5px; margin: 10px 0;">
                    ` : ''}
                    <p style="margin: 5px 0; font-size: 0.85rem; color: #64748b;">
                        ${complaint.address || 'Location: ' + complaint.latitude + ', ' + complaint.longitude}
                    </p>
                    <p style="margin: 10px 0 0 0; font-size: 0.8rem; color: #94a3b8;">
                        Reported: ${new Date(complaint.created_at).toLocaleDateString()}
                    </p>
                </div>
            `;
            
            marker.bindPopup(popupContent);
            markerCluster.addLayer(marker);
            markers.push(marker);
            
            // Update counts
            if (complaint.status === 'Pending') pendingCount++;
            else if (complaint.status === 'In Progress') progressCount++;
            else if (complaint.status === 'Resolved') resolvedCount++;
        }
    });
    
    mainMap.addLayer(markerCluster);
    
    // Update statistics
    document.getElementById('totalCount').textContent = complaintsData.length;
    document.getElementById('pendingCount').textContent = pendingCount;
    document.getElementById('progressCount').textContent = progressCount;
    document.getElementById('resolvedCount').textContent = resolvedCount;
    
    // Fit map to show all markers
    if (markers.length > 0) {
        const group = new L.featureGroup(markers);
        mainMap.fitBounds(group.getBounds().pad(0.1));
    }
    
    // Check for URL parameters to focus on specific location
    const urlParams = new URLSearchParams(window.location.search);
    const lat = urlParams.get('lat');
    const lng = urlParams.get('lng');
    
    if (lat && lng) {
        mainMap.setView([parseFloat(lat), parseFloat(lng)], 15);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initMainMap();
});
