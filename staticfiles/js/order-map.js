const NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search';
const OSRM_URL = 'https://router.project-osrm.org/route/v1/driving';
const DEFAULT_CENTER = [52.5200, 13.4050]; // Berlin, Germany
const DEFAULT_ZOOM = 12;

const geocodeCache = new Map();

async function geocodeAddress(query) {
    const key = query.trim().toLowerCase();
    if (!key) return null;
    if (geocodeCache.has(key)) return geocodeCache.get(key);

    const url = `${NOMINATIM_URL}?format=json&limit=1&countrycodes=de&q=${encodeURIComponent(query + ', Germany')}`;
    const response = await fetch(url, {
        headers: { 'Accept-Language': 'de' },
    });
    if (!response.ok) return null;

    const data = await response.json();
    if (!data.length) return null;

    const result = {
        lat: parseFloat(data[0].lat),
        lng: parseFloat(data[0].lon),
        label: data[0].display_name,
    };
    geocodeCache.set(key, result);
    return result;
}

async function fetchRoute(from, to) {
    const url = `${OSRM_URL}/${from.lng},${from.lat};${to.lng},${to.lat}?overview=full&geometries=geojson`;
    const response = await fetch(url);
    if (!response.ok) return null;

    const data = await response.json();
    if (data.code !== 'Ok' || !data.routes.length) return null;

    const route = data.routes[0];
    const coords = route.geometry.coordinates.map(([lng, lat]) => [lat, lng]);
    return {
        coords,
        distanceKm: route.distance / 1000,
        durationMin: Math.round(route.duration / 60),
    };
}

function createDarkMap(elementId) {
    const map = L.map(elementId, {
        zoomControl: false,
        attributionControl: false,
    }).setView(DEFAULT_CENTER, DEFAULT_ZOOM);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 19,
    }).addTo(map);

    L.control.zoom({ position: 'topright' }).addTo(map);
    L.control.attribution({ position: 'bottomright', prefix: false })
        .addAttribution('© OpenStreetMap · © CARTO')
        .addTo(map);

    return map;
}

function pickupIcon() {
    return L.divIcon({ className: 'map-marker marker-from', html: '<div class="marker-dot"></div>', iconSize: [20,20], iconAnchor: [10,10] });
}

function dropoffIcon() {
    return L.divIcon({ className: 'map-marker marker-to', html: '<div class="marker-dot"></div>', iconSize: [20,20], iconAnchor: [10,10] });
}

function carIcon() {
    return L.divIcon({ className: 'map-marker marker-car', html: '🚕', iconSize: [30,30], iconAnchor: [15,15] });
}

class RideMap {
    constructor(mapElId) {
        this.map = createDarkMap(mapElId);
        this.fromMarker = null;
        this.toMarker = null;
        this.carMarker = null;
        this.routeLine = null;
        this.routeData = null;
    }

    clearRoute() {
        if (this.fromMarker) this.map.removeLayer(this.fromMarker);
        if (this.toMarker) this.map.removeLayer(this.toMarker);
        if (this.carMarker) this.map.removeLayer(this.carMarker);
        if (this.routeLine) this.map.removeLayer(this.routeLine);
        this.fromMarker = this.toMarker = this.carMarker = this.routeLine = null;
        this.routeData = null;
    }

    async buildRoute(fromQuery, toQuery) {
        this.clearRoute();
        const [from, to] = await Promise.all([
            geocodeAddress(fromQuery),
            geocodeAddress(toQuery),
        ]);

        if (!from || !to) return null;

        const route = await fetchRoute(from, to);
        if (!route) return null;

        this.fromMarker = L.marker([from.lat, from.lng], { icon: pickupIcon() }).addTo(this.map);
        this.toMarker = L.marker([to.lat, to.lng], { icon: dropoffIcon() }).addTo(this.map);
        this.routeLine = L.polyline(route.coords, {
            color: '#f5c518',
            weight: 5,
            opacity: 0.9,
        }).addTo(this.map);

        this.map.fitBounds(this.routeLine.getBounds(), { padding: [90, 90] });
        this.routeData = { from, to, ...route };
        return this.routeData;
    }

    showCarAlongRoute(progress = 0.35) {
        if (!this.routeLine) return;
        const latLngs = this.routeLine.getLatLngs();
        const idx = Math.min(latLngs.length - 1, Math.floor(latLngs.length * progress));
        const pos = latLngs[idx];
        if (this.carMarker) this.map.removeLayer(this.carMarker);
        this.carMarker = L.marker(pos, { icon: carIcon() }).addTo(this.map);
    }

    locateUser() {
        if (!navigator.geolocation) return;
        navigator.geolocation.getCurrentPosition((pos) => {
            const { latitude, longitude } = pos.coords;
            this.map.setView([latitude, longitude], 14);
            L.circleMarker([latitude, longitude], {
                radius: 8, color: '#4dabf7', fillColor: '#4dabf7', fillOpacity: 0.8,
            }).addTo(this.map);
        });
    }
}

window.RideMap = RideMap;
window.geocodeAddress = geocodeAddress;
