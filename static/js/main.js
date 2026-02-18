// Main JavaScript for Complaint Form
let map, marker;
let selectedLocation = null;

// Initialize map
function initMap() {
    // Default to India (Jharkhand)
    const defaultLocation = [23.6102, 85.2799];
    
    map = L.map('map').setView(defaultLocation, 7);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Add instruction text on map
    const instructionPopup = L.popup()
        .setLatLng(defaultLocation)
        .setContent('<b>Click anywhere on the map to select your location</b>')
        .openOn(map);
    
    // Add click event to select location
    map.on('click', function(e) {
        setLocation(e.latlng.lat, e.latlng.lng);
        map.closePopup(instructionPopup);
    });
}

// Set location on map
function setLocation(lat, lng) {
    selectedLocation = { lat, lng };
    
    // Remove existing marker
    if (marker) {
        map.removeLayer(marker);
    }
    
    // Add new marker
    marker = L.marker([lat, lng]).addTo(map);
    
    // Update hidden inputs
    document.getElementById('latitude').value = lat;
    document.getElementById('longitude').value = lng;
    
    // Reverse geocode to get address
    fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`)
        .then(response => response.json())
        .then(data => {
            if (data.display_name) {
                document.getElementById('address').value = data.display_name;
            }
        })
        .catch(error => console.error('Geocoding error:', error));
}

// Search by PIN code
document.getElementById('searchPincode').addEventListener('click', function() {
    const pincode = document.getElementById('pincode').value.trim();
    
    if (!pincode) {
        alert('Please enter a PIN code');
        return;
    }
    
    if (!/^\d{6}$/.test(pincode)) {
        alert('Please enter a valid 6-digit PIN code');
        return;
    }
    
    this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
    this.disabled = true;
    
    // Search using Nominatim API
    fetch(`https://nominatim.openstreetmap.org/search?postalcode=${pincode}&country=India&format=json&limit=1`)
        .then(response => response.json())
        .then(data => {
            if (data && data.length > 0) {
                const lat = parseFloat(data[0].lat);
                const lng = parseFloat(data[0].lon);
                const displayName = data[0].display_name;
                
                setLocation(lat, lng);
                map.setView([lat, lng], 13);
                document.getElementById('address').value = displayName;
                
                this.innerHTML = '<i class="fas fa-check"></i> Found!';
                setTimeout(() => {
                    this.innerHTML = '<i class="fas fa-search"></i> Search PIN';
                    this.disabled = false;
                }, 2000);
            } else {
                alert('PIN code not found. Please try another or click on the map.');
                this.innerHTML = '<i class="fas fa-search"></i> Search PIN';
                this.disabled = false;
            }
        })
        .catch(error => {
            console.error('Error searching PIN code:', error);
            alert('Error searching PIN code. Please try again or click on the map.');
            this.innerHTML = '<i class="fas fa-search"></i> Search PIN';
            this.disabled = false;
        });
});

// Allow Enter key to search PIN code
document.getElementById('pincode').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        document.getElementById('searchPincode').click();
    }
});

// Get current location
document.getElementById('getCurrentLocation').addEventListener('click', async function() {
    if (!navigator.geolocation) {
        alert('Geolocation is not supported by your browser. Please use PIN code or click on the map.');
        return;
    }
    
    // Check if we need to request permission
    if (navigator.permissions) {
        try {
            const permissionStatus = await navigator.permissions.query({ name: 'geolocation' });
            
            if (permissionStatus.state === 'denied') {
                alert('Location access is blocked. Please:\n\n1. Click the lock icon 🔒 in the address bar\n2. Allow location access\n3. Refresh the page and try again\n\nOr use PIN code / click on map instead.');
                return;
            }
        } catch (e) {
            console.log('Permission API not supported');
        }
    }
    
    this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Requesting location access...';
    this.disabled = true;
    
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            
            setLocation(lat, lng);
            map.setView([lat, lng], 15);
            
            this.innerHTML = '<i class="fas fa-check"></i> Location Found!';
            this.disabled = false;
            
            setTimeout(() => {
                this.innerHTML = '<i class="fas fa-location-arrow"></i> Use Current Location';
            }, 2000);
        },
        (error) => {
            let errorMsg = '';
            let instructions = '';
            
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    errorMsg = 'Location Access Denied';
                    instructions = 'To enable location:\n\n1. Click the lock icon 🔒 or settings icon in the address bar\n2. Find "Location" permissions\n3. Change to "Allow"\n4. Refresh the page\n\nAlternatively:\n• Enter your PIN code above, or\n• Click anywhere on the map to select location';
                    break;
                case error.POSITION_UNAVAILABLE:
                    errorMsg = 'Location information unavailable';
                    instructions = 'Your device cannot determine your location.\n\nPlease use PIN code or click on the map instead.';
                    break;
                case error.TIMEOUT:
                    errorMsg = 'Location request timed out';
                    instructions = 'Please try again or use PIN code / click on map.';
                    break;
                default:
                    errorMsg = 'An unknown error occurred';
                    instructions = 'Please use PIN code or click on the map.';
            }
            
            alert(errorMsg + '\n\n' + instructions);
            this.innerHTML = '<i class="fas fa-location-arrow"></i> Use Current Location';
            this.disabled = false;
            
            // Zoom to default location
            map.setView([23.6102, 85.2799], 10);
        },
        {
            enableHighAccuracy: true,
            timeout: 15000,
            maximumAge: 0
        }
    );
});

// Image preview
document.getElementById('image').addEventListener('change', function(e) {
    const file = e.target.files[0];
    const preview = document.getElementById('imagePreview');
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
        };
        reader.readAsDataURL(file);
        
        // Update label
        const label = document.querySelector('.file-label span');
        label.textContent = file.name;
    }
});

// Form submission
document.getElementById('complaintForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Validate all required fields
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const category = document.getElementById('category').value;
    const description = document.getElementById('description').value.trim();
    const imageFile = document.getElementById('image').files[0];
    const address = document.getElementById('address').value.trim();
    
    // Check all required fields
    if (!name || !email || !phone || !category || !description || !address) {
        alert('⚠️ Please fill all required fields!');
        return;
    }
    
    // Validate phone number (10 digits)
    if (phone.length !== 10 || !/^[0-9]{10}$/.test(phone)) {
        alert('⚠️ Please enter a valid 10-digit phone number!');
        document.getElementById('phone').focus();
        return;
    }
    
    // Validate image upload (MANDATORY)
    if (!imageFile) {
        alert('⚠️ Image evidence is mandatory! Please upload a photo of the issue.');
        document.getElementById('image').focus();
        return;
    }
    
    // Validate image file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    if (!allowedTypes.includes(imageFile.type)) {
        alert('⚠️ Please upload a valid image file (JPG, PNG, GIF, or WebP)');
        document.getElementById('image').value = '';
        document.getElementById('imagePreview').innerHTML = '';
        return;
    }
    
    // Validate image file size (max 5MB)
    if (imageFile.size > 5 * 1024 * 1024) {
        alert('⚠️ Image size must be less than 5MB!');
        return;
    }
    
    // Validate location
    if (!selectedLocation) {
        alert('⚠️ Please select a location on the map!');
        return;
    }
    
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
    
    const formData = new FormData(this);
    
    try {
        const response = await fetch('/submit-complaint', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showSuccessModal(result);
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        alert('Error submitting complaint: ' + error.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Submit Complaint';
    }
});

// Show success modal
function showSuccessModal(result) {
    const modal = document.getElementById('successModal');
    const modalBody = document.getElementById('modalBody');
    
    let duplicateWarning = '';
    if (result.is_duplicate && result.similar_complaints.length > 0) {
        duplicateWarning = `
            <div style="background: #fef3c7; padding: 1rem; border-radius: 5px; margin-top: 1rem;">
                <strong><i class="fas fa-exclamation-triangle"></i> Similar Complaints Found:</strong>
                <p>We found ${result.similar_complaints.length} similar complaint(s). Your issue will be linked with existing reports for faster resolution.</p>
            </div>
        `;
    }
    
    modalBody.innerHTML = `
        <p style="font-size: 1.1rem; margin-bottom: 1rem;">
            Your complaint has been successfully submitted!
        </p>
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 5px;">
            <p><strong>Complaint ID:</strong> #${result.complaint_id}</p>
            <p><strong>Priority:</strong> <span class="badge badge-${result.priority.toLowerCase()}">${result.priority}</span></p>
            <p style="margin-top: 0.5rem; color: #64748b;">
                Your complaint will be reviewed and assigned to the appropriate department. 
                You will receive updates via email.
            </p>
        </div>
        ${duplicateWarning}
    `;
    
    modal.style.display = 'block';
}

// Close modal
function closeModal() {
    document.getElementById('successModal').style.display = 'none';
}

// Close modal on outside click
window.onclick = function(event) {
    const modal = document.getElementById('successModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initMap();
});
