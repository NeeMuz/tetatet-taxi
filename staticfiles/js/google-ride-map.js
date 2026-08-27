/**
 * Google Maps ride controller — satellite, click-to-set points, directions.
 */
const BERLIN = { lat: 52.5200, lng: 13.4050 };

class GoogleRideMap {
    constructor(mapElId, options = {}) {
        this.mapEl = document.getElementById(mapElId);
        this.geocoder = new google.maps.Geocoder();
        this.directionsService = new google.maps.DirectionsService();
        this.directionsRenderer = new google.maps.DirectionsRenderer({
            suppressMarkers: true,
            polylineOptions: { strokeColor: '#ffffff', strokeWeight: 5, strokeOpacity: 0.9 },
        });

        this.pickupMarker = null;
        this.dropoffMarker = null;
        this.carMarker = null;
        this.pickupPos = null;
        this.dropoffPos = null;
        this.routeData = null;
        this.clickTarget = 'from';
        this.satellite = true;

        this.onRouteUpdate = options.onRouteUpdate || (() => {});
        this.onAddressUpdate = options.onAddressUpdate || (() => {});

        this.map = new google.maps.Map(this.mapEl, {
            center: BERLIN,
            zoom: 12,
            mapTypeId: 'hybrid',
            disableDefaultUI: true,
            zoomControl: false,
            mapTypeControl: false,
            streetViewControl: false,
            fullscreenControl: false,
            clickableIcons: false,
            styles: this._darkStyles(),
        });

        this.directionsRenderer.setMap(this.map);

        this.map.addListener('click', (e) => this._onMapClick(e.latLng));

        document.getElementById('btnSatellite')?.addEventListener('click', () => this.toggleSatellite());
        document.getElementById('btnZoomIn')?.addEventListener('click', () => {
            this.map.setZoom(this.map.getZoom() + 1);
        });
        document.getElementById('btnZoomOut')?.addEventListener('click', () => {
            this.map.setZoom(this.map.getZoom() - 1);
        });
        document.getElementById('locateBtn')?.addEventListener('click', () => this.locateUser());

        setTimeout(() => google.maps.event.trigger(this.map, 'resize'), 300);
    }

    _darkStyles() {
        return [
            { elementType: 'geometry', stylers: [{ color: '#1a1a1a' }] },
            { elementType: 'labels.text.fill', stylers: [{ color: '#ffffff' }] },
            { elementType: 'labels.text.stroke', stylers: [{ color: '#000000' }] },
            { featureType: 'road', elementType: 'geometry', stylers: [{ color: '#2c2c2c' }] },
            { featureType: 'water', elementType: 'geometry', stylers: [{ color: '#0e0e0e' }] },
        ];
    }

    setClickTarget(target) {
        this.clickTarget = target;
        const hint = document.getElementById('mapClickHint');
        if (hint) {
            hint.textContent = target === 'from'
                ? 'Кликните на карте — точка отправления'
                : 'Кликните на карте — точка назначения';
        }
    }

    toggleSatellite() {
        this.satellite = !this.satellite;
        this.map.setMapTypeId(this.satellite ? 'hybrid' : 'roadmap');
        const btn = document.getElementById('btnSatellite');
        if (btn) btn.classList.toggle('active', this.satellite);
    }

    async _onMapClick(latLng) {
        const address = await this._reverseGeocode(latLng);
        if (this.clickTarget === 'from') {
            this.setPickup(latLng, address);
            this.onAddressUpdate('from', address);
            this.setClickTarget('to');
            document.getElementById('to')?.focus();
        } else {
            this.setDropoff(latLng, address);
            this.onAddressUpdate('to', address);
        }
        await this.buildRouteFromMarkers();
    }

    _reverseGeocode(latLng) {
        return new Promise((resolve) => {
            this.geocoder.geocode({ location: latLng }, (results, status) => {
                resolve(status === 'OK' && results[0] ? results[0].formatted_address : `${latLng.lat().toFixed(5)}, ${latLng.lng().toFixed(5)}`);
            });
        });
    }

    _geocodeAddress(address) {
        return new Promise((resolve) => {
            const q = address.includes('Germany') ? address : `${address}, Germany`;
            this.geocoder.geocode({ address: q }, (results, status) => {
                if (status === 'OK' && results[0]) {
                    resolve({ latLng: results[0].geometry.location, address: results[0].formatted_address });
                } else resolve(null);
            });
        });
    }

    _makeMarker(pos, type) {
        const isFrom = type === 'from';
        return new google.maps.Marker({
            position: pos,
            map: this.map,
            draggable: true,
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: isFrom ? 8 : 8,
                fillColor: isFrom ? '#ffffff' : '#888888',
                fillOpacity: 1,
                strokeColor: isFrom ? '#000000' : '#ffffff',
                strokeWeight: 2,
            },
            label: isFrom ? { text: 'A', color: '#000', fontWeight: 'bold', fontSize: '11px' } : { text: 'B', color: '#fff', fontWeight: 'bold', fontSize: '11px' },
        });
    }

    setPickup(latLng, address) {
        if (this.pickupMarker) this.pickupMarker.setMap(null);
        this.pickupPos = latLng;
        this.pickupMarker = this._makeMarker(latLng, 'from');
        this.pickupMarker.addListener('dragend', async () => {
            this.pickupPos = this.pickupMarker.getPosition();
            const addr = await this._reverseGeocode(this.pickupPos);
            this.onAddressUpdate('from', addr);
            await this.buildRouteFromMarkers();
        });
    }

    setDropoff(latLng, address) {
        if (this.dropoffMarker) this.dropoffMarker.setMap(null);
        this.dropoffPos = latLng;
        this.dropoffMarker = this._makeMarker(latLng, 'to');
        this.dropoffMarker.addListener('dragend', async () => {
            this.dropoffPos = this.dropoffMarker.getPosition();
            const addr = await this._reverseGeocode(this.dropoffPos);
            this.onAddressUpdate('to', addr);
            await this.buildRouteFromMarkers();
        });
    }

    async setFromAddress(address) {
        const result = await this._geocodeAddress(address);
        if (!result) return false;
        this.setPickup(result.latLng, result.address);
        this.onAddressUpdate('from', result.address);
        return true;
    }

    async setToAddress(address) {
        const result = await this._geocodeAddress(address);
        if (!result) return false;
        this.setDropoff(result.latLng, result.address);
        this.onAddressUpdate('to', result.address);
        return true;
    }

    async buildRoute(fromText, toText) {
        if (fromText) await this.setFromAddress(fromText);
        if (toText) await this.setToAddress(toText);
        return this.buildRouteFromMarkers();
    }

    buildRouteFromMarkers() {
        return new Promise((resolve) => {
            if (!this.pickupPos || !this.dropoffPos) {
                this.routeData = null;
                this.directionsRenderer.setDirections({ routes: [] });
                this.onRouteUpdate(null);
                resolve(null);
                return;
            }

            this.directionsService.route({
                origin: this.pickupPos,
                destination: this.dropoffPos,
                travelMode: google.maps.TravelMode.DRIVING,
            }, (result, status) => {
                if (status !== 'OK') {
                    this.routeData = null;
                    this.onRouteUpdate(null);
                    resolve(null);
                    return;
                }

                this.directionsRenderer.setDirections(result);
                const leg = result.routes[0].legs[0];
                this.routeData = {
                    distanceKm: leg.distance.value / 1000,
                    durationMin: Math.round(leg.duration.value / 60),
                    fromAddress: leg.start_address,
                    toAddress: leg.end_address,
                };
                this.map.fitBounds(result.routes[0].bounds, 40);
                this.onRouteUpdate(this.routeData);
                resolve(this.routeData);
            });
        });
    }

    showCar(progress = 0.4) {
        if (!this.directionsRenderer.getDirections()?.routes?.length) return;
        const path = this.directionsRenderer.getDirections().routes[0].overview_path;
        const idx = Math.min(path.length - 1, Math.floor(path.length * progress));
        const pos = path[idx];
        if (this.carMarker) this.carMarker.setMap(null);
        this.carMarker = new google.maps.Marker({
            position: pos,
            map: this.map,
            icon: { url: 'data:image/svg+xml,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"><text y="20" font-size="20">🚕</text></svg>'), scaledSize: new google.maps.Size(32, 32) },
        });
    }

    locateUser() {
        if (!navigator.geolocation) return;
        navigator.geolocation.getCurrentPosition(async (pos) => {
            const latLng = { lat: pos.coords.latitude, lng: pos.coords.longitude };
            this.map.setCenter(latLng);
            this.map.setZoom(15);
            const address = await this._reverseGeocode(new google.maps.LatLng(latLng.lat, latLng.lng));
            this.setPickup(new google.maps.LatLng(latLng.lat, latLng.lng), address);
            this.onAddressUpdate('from', address);
            this.setClickTarget('to');
            await this.buildRouteFromMarkers();
        });
    }

    clear() {
        if (this.pickupMarker) this.pickupMarker.setMap(null);
        if (this.dropoffMarker) this.dropoffMarker.setMap(null);
        if (this.carMarker) this.carMarker.setMap(null);
        this.pickupMarker = this.dropoffMarker = this.carMarker = null;
        this.pickupPos = this.dropoffPos = null;
        this.routeData = null;
        this.directionsRenderer.setDirections({ routes: [] });
    }
}

window.GoogleRideMap = GoogleRideMap;
