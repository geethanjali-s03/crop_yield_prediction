/* ============================================
   CropYield AI - Main JavaScript
   General utilities and handlers
   ============================================ */

// ============ Alert & Toast Notifications ============
function showAlert(message, type = 'info', duration = 5000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('main') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    if (duration) {
        setTimeout(() => {
            alertDiv.remove();
        }, duration);
    }
    
    return alertDiv;
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">${message}</div>
    `;
    
    const container = document.getElementById('toast-container') || document.body;
    container.appendChild(toast);
    
    setTimeout(() => toast.remove(), 3000);
}

// ============ Loading States ============
function setLoading(element, isLoading = true) {
    if (isLoading) {
        element.disabled = true;
        const originalText = element.textContent;
        element.setAttribute('data-original-text', originalText);
        element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    } else {
        element.disabled = false;
        const originalText = element.getAttribute('data-original-text') || 'Submit';
        element.textContent = originalText;
    }
}

function showSpinner(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="text-center p-4">
                <div class="spinner-border" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
    }
}

// ============ Form Handling ============
function getFormData(formId) {
    const form = document.getElementById(formId);
    if (!form) return null;
    
    const formData = new FormData(form);
    const data = {};
    
    for (const [key, value] of formData.entries()) {
        if (data[key]) {
            // Handle multiple values (like checkboxes)
            if (Array.isArray(data[key])) {
                data[key].push(value);
            } else {
                data[key] = [data[key], value];
            }
        } else {
            data[key] = value;
        }
    }
    
    return data;
}

function populateForm(formId, data) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    for (const [key, value] of Object.entries(data)) {
        const element = form.elements[key];
        if (element) {
            if (element.type === 'checkbox') {
                element.checked = value;
            } else {
                element.value = value;
            }
        }
    }
}

function validateForm(formId, rules = {}) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    // Clear previous errors
    form.querySelectorAll('.error-message').forEach(el => el.remove());
    form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
    
    let isValid = true;
    
    // HTML5 validation
    if (!form.checkValidity()) {
        isValid = false;
        form.querySelectorAll(':invalid').forEach(el => {
            el.classList.add('is-invalid');
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message text-danger';
            errorDiv.textContent = el.validationMessage;
            el.parentElement.appendChild(errorDiv);
        });
    }
    
    // Custom validation rules
    for (const [fieldName, rule] of Object.entries(rules)) {
        const field = form.elements[fieldName];
        if (!field) continue;
        
        const value = field.value.trim();
        
        if (rule.required && !value) {
            isValid = false;
            field.classList.add('is-invalid');
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message text-danger';
            errorDiv.textContent = rule.message || 'This field is required';
            field.parentElement.appendChild(errorDiv);
        }
        
        if (rule.min && value && value.length < rule.min) {
            isValid = false;
            field.classList.add('is-invalid');
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message text-danger';
            errorDiv.textContent = `Minimum length: ${rule.min}`;
            field.parentElement.appendChild(errorDiv);
        }
        
        if (rule.pattern && value && !rule.pattern.test(value)) {
            isValid = false;
            field.classList.add('is-invalid');
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message text-danger';
            errorDiv.textContent = rule.message || 'Invalid format';
            field.parentElement.appendChild(errorDiv);
        }
    }
    
    return isValid;
}

// ============ API Calls ============
async function apiCall(url, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call error:', error);
        throw error;
    }
}

// ============ Table Utilities ============
function populateTable(tableId, data) {
    const tbody = document.querySelector(`#${tableId} tbody`);
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="100%" class="text-center">No data available</td></tr>';
        return;
    }
    
    data.forEach(row => {
        const tr = document.createElement('tr');
        for (const value of Object.values(row)) {
            const td = document.createElement('td');
            td.textContent = value;
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    });
}

function exportTableToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    
    // Get headers
    const headers = [];
    table.querySelectorAll('thead th').forEach(th => {
        headers.push(th.textContent);
    });
    csv.push(headers.join(','));
    
    // Get rows
    table.querySelectorAll('tbody tr').forEach(tr => {
        const row = [];
        tr.querySelectorAll('td').forEach(td => {
            row.push(`"${td.textContent}"`);
        });
        csv.push(row.join(','));
    });
    
    // Download
    const link = document.createElement('a');
    link.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv.join('\n'));
    link.download = filename;
    link.click();
}

function printTable(tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const printWindow = window.open('', '', 'height=400,width=800');
    printWindow.document.write('<html><head><title>Print</title>');
    printWindow.document.write('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5/dist/css/bootstrap.min.css" rel="stylesheet">');
    printWindow.document.write('</head><body>');
    printWindow.document.write(table.outerHTML);
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    printWindow.print();
}

// ============ Chart Utilities ============
function createChart(canvasId, type, labels, datasets, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    return new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: datasets.map(dataset => ({
                ...dataset,
                backgroundColor: dataset.backgroundColor || `rgba(46, 204, 113, 0.2)`,
                borderColor: dataset.borderColor || 'rgba(46, 204, 113, 1)',
                borderWidth: 2
            }))
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            ...options
        }
    });
}

// ============ Date & Time Utilities ============
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDateTime(date) {
    return new Date(date).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function getTimeAgo(date) {
    const seconds = Math.floor((new Date() - new Date(date)) / 1000);
    
    let interval = seconds / 31536000;
    if (interval > 1) return Math.floor(interval) + 'y';
    
    interval = seconds / 2592000;
    if (interval > 1) return Math.floor(interval) + 'mo';
    
    interval = seconds / 86400;
    if (interval > 1) return Math.floor(interval) + 'd';
    
    interval = seconds / 3600;
    if (interval > 1) return Math.floor(interval) + 'h';
    
    interval = seconds / 60;
    if (interval > 1) return Math.floor(interval) + 'm';
    
    return Math.floor(seconds) + 's';
}

// ============ DOM Utilities ============
function addClass(selector, className) {
    document.querySelectorAll(selector).forEach(el => {
        el.classList.add(className);
    });
}

function removeClass(selector, className) {
    document.querySelectorAll(selector).forEach(el => {
        el.classList.remove(className);
    });
}

function toggleClass(selector, className) {
    document.querySelectorAll(selector).forEach(el => {
        el.classList.toggle(className);
    });
}

// ============ Local Storage Utilities ============
const Storage = {
    set: (key, value) => {
        localStorage.setItem(key, JSON.stringify(value));
    },
    
    get: (key) => {
        const value = localStorage.getItem(key);
        return value ? JSON.parse(value) : null;
    },
    
    remove: (key) => {
        localStorage.removeItem(key);
    },
    
    clear: () => {
        localStorage.clear();
    }
};

// ============ Analytics & Tracking ============
function trackEvent(eventName, eventData = {}) {
    // Send to server for analytics
    fetch('/api/analytics', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            event: eventName,
            data: eventData,
            timestamp: new Date().toISOString()
        })
    }).catch(err => console.error('Analytics error:', err));
}

// ============ Initialize Page ============
document.addEventListener('DOMContentLoaded', () => {
    // Add active class to current nav link
    const currentPath = window.location.pathname;
    document.querySelectorAll('nav a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Initialize tooltips
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
        new bootstrap.Tooltip(el);
    });
    
    // Initialize popovers
    document.querySelectorAll('[data-bs-toggle="popover"]').forEach(el => {
        new bootstrap.Popover(el);
    });
    
    // Add animation to elements on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    });
    
    document.querySelectorAll('[data-animate]').forEach(el => {
        observer.observe(el);
    });
});
