// Dashboard functionality for AI Resume Screening Tool

class DashboardManager {
    constructor() {
        this.initializeEventListeners();
        this.loadInitialData();
    }

    initializeEventListeners() {
        // File upload validation
        const fileInput = document.getElementById('resume');
        if (fileInput) {
            fileInput.addEventListener('change', this.validateFileUpload);
        }

        // Bulk upload functionality
        const bulkUploadBtn = document.getElementById('bulk-upload');
        if (bulkUploadBtn) {
            bulkUploadBtn.addEventListener('click', this.handleBulkUpload);
        }

        // Search and filter functionality
        const searchInput = document.getElementById('search-resumes');
        if (searchInput) {
            searchInput.addEventListener('input', this.filterResults);
        }
    }

    validateFileUpload(event) {
        const file = event.target.files[0];
        const maxSize = 16 * 1024 * 1024; // 16MB
        const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];

        if (file) {
            if (file.size > maxSize) {
                alert('File size exceeds 16MB limit. Please choose a smaller file.');
                event.target.value = '';
                return false;
            }

            if (!allowedTypes.includes(file.type)) {
                alert('Invalid file type. Please upload PDF, DOCX, or TXT files only.');
                event.target.value = '';
                return false;
            }

            // Show file preview
            const preview = document.getElementById('file-preview');
            if (preview) {
                preview.innerHTML = `
                    <div class="alert alert-info">
                        <i class="fas fa-file"></i> ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)
                    </div>
                `;
            }
        }
    }

    async handleBulkUpload() {
        const fileInput = document.getElementById('bulk-files');
        const jobDescription = document.getElementById('job_description').value;
        
        if (!fileInput.files.length) {
            alert('Please select files to upload.');
            return;
        }

        const formData = new FormData();
        for (let file of fileInput.files) {
            formData.append('resumes', file);
        }
        formData.append('job_description', jobDescription);

        try {
            this.showLoadingSpinner();
            const response = await fetch('/api/bulk_process', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (response.ok) {
                this.displayBulkResults(data.results);
            } else {
                throw new Error(data.error || 'Processing failed');
            }
        } catch (error) {
            alert('Error processing files: ' + error.message);
        } finally {
            this.hideLoadingSpinner();
        }
    }

    displayBulkResults(results) {
        const container = document.getElementById('bulk-results');
        if (!container) return;

        let html = '<div class="table-responsive"><table class="table table-striped">';
        html += '<thead><tr><th>File</th><th>Score</th><th>Status</th><th>Skills</th><th>Experience</th></tr></thead>';
        html += '<tbody>';

        results.forEach(result => {
            const statusClass = this.getStatusClass(result.status);
            html += `
                <tr>
                    <td>${result.filename}</td>
                    <td><span class="badge bg-${statusClass}">${result.overall_score}</span></td>
                    <td><span class="badge bg-${statusClass}">${result.status}</span></td>
                    <td>${result.skills.length}</td>
                    <td>${result.experience_years} years</td>
                </tr>
            `;
        });

        html += '</tbody></table></div>';
        container.innerHTML = html;

        // Show summary chart
        this.createBulkResultsChart(results);
    }

    getStatusClass(status) {
        const statusMap = {
            'Excellent': 'success',
            'Good': 'info',
            'Fair': 'warning',
            'Poor': 'danger'
        };
        return statusMap[status] || 'secondary';
    }

    createBulkResultsChart(results) {
        const statusCounts = results.reduce((acc, result) => {
            acc[result.status] = (acc[result.status] || 0) + 1;
            return acc;
        }, {});

        const chartData = [{
            values: Object.values(statusCounts),
            labels: Object.keys(statusCounts),
            type: 'pie',
            marker: {
                colors: ['#28a745', '#17a2b8', '#ffc107', '#dc3545']
            }
        }];

        const layout = {
            title: 'Bulk Processing Results',
            height: 400
        };

        const chartContainer = document.getElementById('bulk-chart');
        if (chartContainer) {
            Plotly.newPlot('bulk-chart', chartData, layout);
        }
    }

    filterResults() {
        const searchTerm = document.getElementById('search-resumes').value.toLowerCase();
        const rows = document.querySelectorAll('#results-table tbody tr');

        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            const shouldShow = text.includes(searchTerm);
            row.style.display = shouldShow ? '' : 'none';
        });
    }

    showLoadingSpinner() {
        const spinner = document.getElementById('loading-spinner');
        if (spinner) {
            spinner.style.display = 'block';
        }

        // Disable submit buttons
        const submitButtons = document.querySelectorAll('button[type="submit"]');
        submitButtons.forEach(btn => {
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
        });
    }

    hideLoadingSpinner() {
        const spinner = document.getElementById('loading-spinner');
        if (spinner) {
            spinner.style.display = 'none';
        }

        // Re-enable submit buttons
        const submitButtons = document.querySelectorAll('button[type="submit"]');
        submitButtons.forEach(btn => {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-cogs"></i> Screen Resume';
        });
    }

    async loadInitialData() {
        // Load dashboard analytics on page load
        if (document.getElementById('total-resumes')) {
            try {
                const response = await fetch('/api/analytics');
                const data = await response.json();
                this.updateDashboardCards(data);
            } catch (error) {
                console.error('Error loading analytics:', error);
            }
        }
    }

    updateDashboardCards(data) {
        const elements = [
            { id: 'total-resumes', value: data.total_resumes },
            { id: 'excellent-matches', value: data.excellent_matches },
            { id: 'good-matches', value: data.good_matches },
            { id: 'fair-matches', value: data.fair_matches }
        ];

        elements.forEach(element => {
            const el = document.getElementById(element.id);
            if (el) {
                el.textContent = element.value;
            }
        });
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new DashboardManager();
});

// Utility functions
function exportResults(format) {
    const results = document.getElementById('results-table');
    if (!results) return;

    if (format === 'csv') {
        downloadCSV();
    } else if (format === 'pdf') {
        downloadPDF();
    }
}

function downloadCSV() {
    // Implementation for CSV export
    console.log('CSV export functionality would be implemented here');
}

function downloadPDF() {
    // Implementation for PDF export
    console.log('PDF export functionality would be implemented here');
}

// Real-time updates (if implementing WebSocket)
function initializeWebSocket() {
    // WebSocket implementation for real-time dashboard updates
    // This would be useful for a production environment
    console.log('WebSocket initialization would be implemented here');
}