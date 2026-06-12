/* ============================================
   CropYield AI - Map Handler
   Uses Leaflet.js for interactive maps
   ============================================ */

class MapLocationPicker {
    constructor(mapElementId, options = {}) {
        this.mapElementId = mapElementId;
        this.map = null;
        this.marker = null;
        this.selectedLocation = null;
        this.options = {
            defaultZoom: 12,
            defaultCenter: [20, 78.5], // India center
            ...options
        };
        this.initializeMap();
    }
    
    initializeMap() {
        // Check if Leaflet is available
        if (typeof L === 'undefined') {
            console.error('Leaflet library not loaded');
            this.loadLeaflet();
            return;
        }
        
        this.map = L.map(this.mapElementId).setView(
            this.options.defaultCenter,
            this.options.defaultZoom
        );
        
        // Add tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19,
        }).addTo(this.map);
        
        // Add click listener
        this.map.on('click', (e) => this.handleMapClick(e));
        
        // Add geolocation button
        this.addGeolocationButton();
    }
    
    loadLeaflet() {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css';
        document.head.appendChild(link);
        
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js';
        script.onload = () => this.initializeMap();
        document.head.appendChild(script);
    }
    
    handleMapClick(e) {
        const {lat, lng} = e.latlng;
        this.setLocation(lat, lng);
        this.onLocationSelected?.({lat, lng});
    }
    
    setLocation(lat, lng) {
        this.selectedLocation = {lat, lng};
        
        // Remove old marker
        if (this.marker) {
            this.map.removeLayer(this.marker);
        }
        
        // Add new marker
        this.marker = L.marker([lat, lng], {
            draggable: true
        }).addTo(this.map);
        
        // Update marker position on drag
        this.marker.on('dragend', () => {
            const position = this.marker.getLatLng();
            this.selectedLocation = {lat: position.lat, lng: position.lng};
            this.onLocationSelected?.({lat: position.lat, lng: position.lng});
        });
        
        // Center map on marker
        this.map.setView([lat, lng], this.options.defaultZoom);
        
        // Show popup
        this.marker.bindPopup(`Lat: ${lat.toFixed(4)}, Lng: ${lng.toFixed(4)}`).openPopup();
    }
    
    getSelectedLocation() {
        return this.selectedLocation;
    }
    
    addGeolocationButton() {
        const button = document.createElement('button');
        button.innerHTML = '📍 Use Current Location';
        button.className = 'btn btn-primary';
        button.style.position = 'absolute';
        button.style.top = '10px';
        button.style.right = '10px';
        button.style.zIndex = '1000';
        
        button.addEventListener('click', () => this.getUserLocation());
        
        const container = document.getElementById(this.mapElementId);
        container.style.position = 'relative';
        container.appendChild(button);
    }
    
    getUserLocation() {
        if (!navigator.geolocation) {
            alert('Geolocation not supported by your browser');
            return;
        }
        
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const {latitude, longitude} = position.coords;
                this.setLocation(latitude, longitude);
            },
            (error) => {
                console.error('Geolocation error:', error);
                alert('Unable to get your location');
            }
        );
    }
    
    searchLocation(query) {
        // Using OpenStreetMap Nominatim API (free)
        fetch(`https://nominatim.openstreetmap.org/search?q=${query},India&format=json`)
            .then(response => response.json())
            .then(results => {
                if (results.length > 0) {
                    const {lat, lon} = results[0];
                    this.setLocation(parseFloat(lat), parseFloat(lon));
                } else {
                    alert('Location not found');
                }
            })
            .catch(error => console.error('Error searching location:', error));
    }
    
    onLocationSelected = null;
}

// Helper function to initialize map picker
function initializeMapPicker(mapElementId, onLocationSelected) {
    if (!document.getElementById(mapElementId)) {
        console.error(`Map element ${mapElementId} not found`);
        return null;
    }
    
    const picker = new MapLocationPicker(mapElementId);
    if (onLocationSelected) {
        picker.onLocationSelected = onLocationSelected;
    }
    return picker;
}

// Attach map picker to location input
function attachLocationSearch(inputElementId, mapElementId) {
    const inputElement = document.getElementById(inputElementId);
    const mapElement = document.getElementById(mapElementId);
    
    if (!inputElement || !mapElement) return;
    
    const picker = new MapLocationPicker(mapElementId);
    
    inputElement.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            picker.searchLocation(inputElement.value);
        }
    });
    
    return picker;
}

// Get location from coordinates
async function getLocationName(lat, lng) {
    try {
        const response = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`
        );
        const data = await response.json();
        return data.address?.city || data.address?.town || data.address?.village || 'Unknown';
    } catch (error) {
        console.error('Error getting location name:', error);
        return 'Unknown Location';
    }
}

// Distance calculation (Haversine formula)
function calculateDistance(lat1, lng1, lat2, lng2) {
    const R = 6371; // Earth's radius in km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLng = (lng2 - lng1) * Math.PI / 180;
    
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLng / 2) * Math.sin(dLng / 2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c; // Distance in km
}

// Initialize on page load if map element exists
document.addEventListener('DOMContentLoaded', () => {
    // Auto-initialize all map containers with class 'crop-map'
    const mapContainers = document.querySelectorAll('[data-map-id]');
    mapContainers.forEach(container => {
        const mapId = container.getAttribute('data-map-id');
        if (mapId) {
            setTimeout(() => {
                try {
                    new MapLocationPicker(mapId);
                } catch (e) {
                    console.error(`Error initializing map ${mapId}:`, e);
                }
            }, 100);
        }
    });
});
