// Admin Dashboard JavaScript
let currentComplaintId = null;

// Initialize charts
function initCharts() {
    // Category Chart
    const categoryCtx = document.getElementById('categoryChart').getContext('2d');
    const categoryData = statsData.by_category || {};
    
    new Chart(categoryCtx, {
        type: 'pie',
        data: {
            labels: Object.keys(categoryData),
            datasets: [{
                data: Object.values(categoryData),
                backgroundColor: [
                    '#ef4444', '#f59e0b', '#10b981', '#06b6d4', '#8b5cf6',
                    '#ec4899', '#14b8a6', '#f97316', '#6366f1', '#84cc16'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
    
    // Priority Chart
    const priorityCtx = document.getElementById('priorityChart').getContext('2d');
    const priorityData = statsData.by_priority || {};
    
    new Chart(priorityCtx, {
        type: 'bar',
        data: {
            labels: Object.keys(priorityData),
            datasets: [{
                label: 'Number of Complaints',
                data: Object.values(priorityData),
                backgroundColor: [
                    '#ef4444', '#f59e0b', '#06b6d4', '#64748b'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
}

// Filter complaints
function filterComplaints() {
    const statusFilter = document.getElementById('statusFilter').value;
    const priorityFilter = document.getElementById('priorityFilter').value;
    const categoryFilter = document.getElementById('categoryFilter').value;
    
    const rows = document.querySelectorAll('#complaintsTable tbody tr');
    
    rows.forEach(row => {
        const status = row.dataset.status;
        const priority = row.dataset.priority;
        const category = row.dataset.category;
        
        const matchStatus = !statusFilter || status === statusFilter;
        const matchPriority = !priorityFilter || priority === priorityFilter;
        const matchCategory = !categoryFilter || category === categoryFilter;
        
        if (matchStatus && matchPriority && matchCategory) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Add event listeners to filters
document.getElementById('statusFilter').addEventListener('change', filterComplaints);
document.getElementById('priorityFilter').addEventListener('change', filterComplaints);
document.getElementById('categoryFilter').addEventListener('change', filterComplaints);

// View complaint details
async function viewComplaint(id) {
    try {
        const response = await fetch(`/api/complaints/${id}`);
        const result = await response.json();
        
        if (result.success) {
            const complaint = result.complaint;
            const modal = document.getElementById('viewModal');
            const detailsDiv = document.getElementById('complaintDetails');
            
            const imageSection = complaint.image_url ? `
                <div style="margin-top: 1rem;">
                    <strong><i class="fas fa-camera"></i> Evidence Image:</strong><br>
                    <div style="margin-top: 0.5rem; position: relative;">
                        <img src="${complaint.image_url}" 
                             style="max-width: 100%; max-height: 400px; border-radius: 10px; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.1);" 
                             onclick="window.open('${complaint.image_url}', '_blank')" 
                             title="Click to view full size">
                        <div style="margin-top: 0.5rem;">
                            <a href="${complaint.image_url}" download class="btn btn-secondary" style="font-size: 0.9rem;">
                                <i class="fas fa-download"></i> Download Image
                            </a>
                            <button onclick="window.open('${complaint.image_url}', '_blank')" class="btn btn-secondary" style="font-size: 0.9rem; margin-left: 0.5rem;">
                                <i class="fas fa-expand"></i> View Full Size
                            </button>
                        </div>
                    </div>
                </div>
            ` : '<div style="margin-top: 1rem; padding: 1rem; background: #f8fafc; border-radius: 5px; color: #64748b;"><i class="fas fa-image"></i> No image evidence provided</div>';
            
            const duplicateWarning = complaint.is_duplicate ? `
                <div style="background: #fef3c7; padding: 1rem; border-radius: 5px; margin-top: 1rem;">
                    <i class="fas fa-exclamation-triangle"></i> 
                    <strong>Duplicate/Similar:</strong> ${complaint.similar_count} similar complaint(s) found
                </div>
            ` : '';
            
            detailsDiv.innerHTML = `
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div>
                        <p><strong>Complaint ID:</strong> #${complaint.id}</p>
                        <p><strong>Name:</strong> ${complaint.name}</p>
                        <p><strong>Email:</strong> ${complaint.email}</p>
                        <p><strong>Phone:</strong> ${complaint.phone || 'N/A'}</p>
                    </div>
                    <div>
                        <p><strong>Category:</strong> <span class="badge badge-info">${complaint.category}</span></p>
                        <p><strong>Priority:</strong> <span class="badge badge-${complaint.priority.toLowerCase()}">${complaint.priority}</span></p>
                        <p><strong>Status:</strong> <span class="badge badge-status-${complaint.status.toLowerCase().replace(' ', '-')}">${complaint.status}</span></p>
                        <p><strong>Department:</strong> ${complaint.department}</p>
                    </div>
                </div>
                
                <div style="margin-top: 1rem;">
                    <strong>Description:</strong>
                    <p style="background: #f8fafc; padding: 1rem; border-radius: 5px; margin-top: 0.5rem;">
                        ${complaint.description}
                    </p>
                </div>
                
                <div style="margin-top: 1rem;">
                    <strong>Location:</strong>
                    <p>${complaint.address || 'N/A'}</p>
                    <p>Coordinates: ${complaint.latitude}, ${complaint.longitude}</p>
                    <button onclick="showOnMap(${complaint.latitude}, ${complaint.longitude})" class="btn btn-secondary" style="margin-top: 0.5rem;">
                        <i class="fas fa-map-marker-alt"></i> Show on Map
                    </button>
                </div>
                
                ${imageSection}
                ${duplicateWarning}
                
                <div style="margin-top: 1rem;">
                    <p><strong>Submitted:</strong> ${new Date(complaint.created_at).toLocaleString()}</p>
                    <p><strong>Last Updated:</strong> ${new Date(complaint.updated_at).toLocaleString()}</p>
                </div>
            `;
            
            modal.style.display = 'block';
        }
    } catch (error) {
        alert('Error loading complaint details: ' + error.message);
    }
}

// Close view modal
function closeViewModal() {
    document.getElementById('viewModal').style.display = 'none';
}

// Update status
function updateStatus(id) {
    currentComplaintId = id;
    document.getElementById('updateComplaintId').value = id;
    document.getElementById('updateModal').style.display = 'block';
}

// Close update modal
function closeUpdateModal() {
    document.getElementById('updateModal').style.display = 'none';
    currentComplaintId = null;
}

// Handle update form submission
document.getElementById('updateForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const id = document.getElementById('updateComplaintId').value;
    const status = document.getElementById('updateStatus').value;
    const notes = document.getElementById('updateNotes').value;
    
    try {
        const response = await fetch(`/api/complaints/${id}/update`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status, notes })
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Complaint updated successfully!');
            closeUpdateModal();
            location.reload();
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        alert('Error updating complaint: ' + error.message);
    }
});

// Show on map
function showOnMap(lat, lng) {
    window.open(`/map?lat=${lat}&lng=${lng}`, '_blank');
}

// Delete complaint
async function deleteComplaint(id) {
    if (!confirm(`Are you sure you want to delete Complaint #${id}?\n\nThis action cannot be undone!`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/complaints/${id}/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Complaint deleted successfully!');
            location.reload();
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        alert('Error deleting complaint: ' + error.message);
    }
}

// Quick view complaint image
function viewComplaintImage(id, imageUrl) {
    const modal = document.getElementById('viewModal');
    const detailsDiv = document.getElementById('complaintDetails');
    
    detailsDiv.innerHTML = `
        <div style="text-align: center;">
            <h3 style="margin-bottom: 1rem;"><i class="fas fa-image"></i> Complaint #${id} - Evidence Image</h3>
            <img src="${imageUrl}" 
                 style="max-width: 100%; max-height: 70vh; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); cursor: pointer;" 
                 onclick="window.open('${imageUrl}', '_blank')"
                 title="Click to view full size">
            <div style="margin-top: 1.5rem; display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                <a href="${imageUrl}" download class="btn btn-primary">
                    <i class="fas fa-download"></i> Download Image
                </a>
                <button onclick="window.open('${imageUrl}', '_blank')" class="btn btn-secondary">
                    <i class="fas fa-expand"></i> Open in New Tab
                </button>
                <button onclick="viewComplaint(${id})" class="btn btn-secondary">
                    <i class="fas fa-info-circle"></i> View Full Details
                </button>
            </div>
        </div>
    `;
    
    modal.style.display = 'block';
}

// Refresh data
async function refreshData() {
    location.reload();
}

// Close modals on outside click
window.onclick = function(event) {
    const viewModal = document.getElementById('viewModal');
    const updateModal = document.getElementById('updateModal');
    
    if (event.target == viewModal) {
        viewModal.style.display = 'none';
    }
    if (event.target == updateModal) {
        updateModal.style.display = 'none';
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    if (typeof statsData !== 'undefined') {
        initCharts();
    }
});

// Auto-refresh every 30 seconds
setInterval(() => {
    // Only refresh if no modal is open
    if (document.getElementById('viewModal').style.display === 'none' &&
        document.getElementById('updateModal').style.display === 'none') {
        refreshData();
    }
}, 30000);
