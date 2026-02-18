// Public Dashboard JavaScript (Read-only version)

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

// View complaint details (read-only)
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
                    <strong>Evidence:</strong><br>
                    <img src="${complaint.image_url}" style="max-width: 100%; border-radius: 5px; margin-top: 0.5rem;">
                </div>
            ` : '';
            
            detailsDiv.innerHTML = `
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div>
                        <p><strong>Complaint ID:</strong> #${complaint.id}</p>
                        <p><strong>Submitted By:</strong> ${complaint.name}</p>
                        <p><strong>Contact:</strong> ${complaint.email}</p>
                    </div>
                    <div>
                        <p><strong>Category:</strong> <span class="badge badge-info">${complaint.category}</span></p>
                        <p><strong>Priority:</strong> <span class="badge badge-${complaint.priority.toLowerCase()}">${complaint.priority}</span></p>
                        <p><strong>Status:</strong> <span class="badge badge-status-${complaint.status.toLowerCase().replace(' ', '-')}">${complaint.status}</span></p>
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
                </div>
                
                ${imageSection}
                
                <div style="margin-top: 1rem;">
                    <p><strong>Reported:</strong> ${new Date(complaint.created_at).toLocaleString()}</p>
                    <p><strong>Last Updated:</strong> ${new Date(complaint.updated_at).toLocaleString()}</p>
                </div>
            `;
            
            modal.style.display = 'block';
        }
    } catch (error) {
        alert('Error loading complaint details');
    }
}

// Close modal
function closeViewModal() {
    document.getElementById('viewModal').style.display = 'none';
}

// Show on map
function showOnMap(lat, lng) {
    window.open(`/map?lat=${lat}&lng=${lng}`, '_blank');
}

// Close modal on outside click
window.onclick = function(event) {
    const viewModal = document.getElementById('viewModal');
    if (event.target == viewModal) {
        viewModal.style.display = 'none';
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    if (typeof statsData !== 'undefined') {
        initCharts();
    }
});

// Auto-refresh every 60 seconds
setInterval(() => {
    if (document.getElementById('viewModal').style.display === 'none') {
        location.reload();
    }
}, 60000);
