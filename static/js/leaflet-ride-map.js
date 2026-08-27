/**
 * Leaflet maps — бесплатно, без API-ключей.
 */
const BERLIN = [52.5200, 13.4050];
const NOMINATIM = 'https://nominatim.openstreetmap.org';
const OSRM = 'https://router.project-osrm.org/route/v1/driving';

const TILES = {
    dark: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    satellite: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
};

const geocodeCache = new Map();

function mapT(key, fallback) {
    return (window.TETATET_I18N && window.TETATET_I18N[key]) || fallback;
}

async function reverseGeocode(lat, lng) {
    const url = `${NOMINATIM}/reverse?format=json&lat=${lat}&lon=${lng}&accept-language=de`;
    try {
        const res = await fetch(url);
        if (!res.ok) return `${lat.toFixed(5)}, ${lng.toFixed(5)}`;
        const data = await res.json();
        return data.display_name || `${lat.toFixed(5)}, ${lng.toFixed(5)}`;
    } catch {
        return `${lat.toFixed(5)}, ${lng.toFixed(5)}`;
    }
}

async function geocodeAddress(query) {
    const key = query.trim().toLowerCase();
    if (!key) return null;
    if (geocodeCache.has(key)) return geocodeCache.get(key);

    const trySearch = async (q, countrycodes) => {
        const params = new URLSearchParams({ format: 'json', limit: '1', q });
        if (countrycodes) params.set('countrycodes', countrycodes);
        const url = `${NOMINATIM}/search?${params}`;
        const res = await fetch(url, { headers: { 'Accept-Language': 'de' } });
        if (!res.ok) return null;
        const data = await res.json();
        if (!data.length) return null;
        return {
            lat: parseFloat(data[0].lat),
            lng: parseFloat(data[0].lon),
            address: data[0].display_name,
        };
    };

    try {
        const localQ = query.includes('Germany') || query.includes('Deutschland')
            ? query
            : `${query}, Germany`;
        let result = await trySearch(localQ, 'de');
        if (!result) result = await trySearch(query, null);
        if (result) geocodeCache.set(key, result);
        return result;
    } catch {
        return null;
    }
}

async function fetchRoute(from, to) {
    const url = `${OSRM}/${from.lng},${from.lat};${to.lng},${to.lat}?overview=full&geometries=geojson`;
    try {
        const res = await fetch(url);
        if (!res.ok) return null;
        const data = await res.json();
        if (data.code !== 'Ok' || !data.routes.length) return null;
        const route = data.routes[0];
        return {
            coords: route.geometry.coordinates.map(([lng, lat]) => [lat, lng]),
            distanceKm: route.distance / 1000,
            durationMin: Math.round(route.duration / 60),
        };
    } catch {
        return null;
    }
}

function markerIcon(label, filled) {
    return L.divIcon({
        className: 'lf-marker',
        html: `<div class="lf-pin ${filled ? 'lf-pin-b' : 'lf-pin-a'}">${label}</div>`,
        iconSize: [28, 28],
        iconAnchor: [14, 14],
    });
}

const LOCATE_ICON_SVG = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg>`;
const SATELLITE_ICON_SVG = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/></svg>`;

class LeafletRideMap {
    constructor(mapElId, options = {}) {
        this.clickTarget = 'from';
        this.satellite = true;
        this.readOnly = !!options.readOnly;
        this.routeData = null;
        this.pickupPos = null;
        this.dropoffPos = null;
        this.userCircle = null;
        this.userMarker = null;
        this._routeRequestId = 0;
        this._satelliteBtn = null;
        this.onRouteUpdate = options.onRouteUpdate || (() => {});
        this.onAddressUpdate = options.onAddressUpdate || (() => {});

        this.map = L.map(mapElId, { center: BERLIN, zoom: 12, zoomControl: false, attributionControl: false });
        this.layerDark = L.tileLayer(TILES.dark, { maxZoom: 19 });
        this.layerSatellite = L.tileLayer(TILES.satellite, { maxZoom: 19 });
        this.layerSatellite.addTo(this.map);

        L.control.attribution({ position: 'bottomright', prefix: false })
            .addAttribution('© OpenStreetMap · Esri').addTo(this.map);

        this.fromMarker = null;
        this.toMarker = null;
        this.carMarker = null;
        this.routeLine = null;
        this.approachLine = null;
        this.approachPath = null;
        this.tripPath = null;
        this._activeCarPath = null;
        this._carAnimFrame = null;

        if (!this.readOnly) {
            this.map.on('click', (e) => this._onClick(e.latlng));
        }
        this._addMapControls(options);

        const mapEl = document.getElementById(mapElId);
        if (mapEl?.parentElement && window.ResizeObserver) {
            this._resizeObserver = new ResizeObserver(() => {
                this.map.invalidateSize();
            });
            this._resizeObserver.observe(mapEl.parentElement);
        }

        setTimeout(() => this.map.invalidateSize(), 300);

        if (options.locateOnLoad) {
            setTimeout(() => this.locateUser({ silent: true }), 500);
        }
    }

    _addMapControls(options) {
        L.control.zoom({ position: 'topright' }).addTo(this.map);

        const self = this;
        const SatelliteControl = L.Control.extend({
            options: { position: 'topleft' },
            onAdd() {
                const wrap = L.DomUtil.create('div', 'leaflet-bar leaflet-control tetatet-satellite-control');
                const btn = L.DomUtil.create('button', 'tetatet-satellite-btn active', wrap);
                btn.type = 'button';
                btn.title = mapT('map_satellite_title', 'Спутник / Карта');
                btn.setAttribute('aria-label', mapT('map_satellite_aria', 'Переключить вид карты'));
                btn.innerHTML = SATELLITE_ICON_SVG;
                self._satelliteBtn = btn;
                L.DomEvent.disableClickPropagation(wrap);
                L.DomEvent.on(btn, 'click', (e) => {
                    L.DomEvent.stop(e);
                    self.toggleSatellite();
                });
                return wrap;
            },
        });
        new SatelliteControl().addTo(this.map);

        if (options.showLocate !== false) {
            const LocateControl = L.Control.extend({
                options: { position: 'bottomleft' },
                onAdd() {
                    const wrap = L.DomUtil.create('div', 'leaflet-bar leaflet-control tetatet-locate-control');
                    const btn = L.DomUtil.create('button', 'tetatet-locate-btn', wrap);
                    btn.type = 'button';
                    btn.id = 'locateBtn';
                    btn.title = mapT('map_locate_title', 'Моё местоположение');
                    btn.setAttribute('aria-label', mapT('map_locate_title', 'Моё местоположение'));
                    btn.innerHTML = `${LOCATE_ICON_SVG}<span>${mapT('map_locate_btn', 'Моя локация')}</span>`;
                    L.DomEvent.disableClickPropagation(wrap);
                    L.DomEvent.on(btn, 'click', (e) => {
                        L.DomEvent.stop(e);
                        self.locateUser();
                    });
                    return wrap;
                },
            });
            new LocateControl().addTo(this.map);
        }
    }

    setClickTarget(target) {
        this.clickTarget = target;
        const hint = document.getElementById('mapClickHint');
        if (hint) {
            hint.textContent = target === 'from'
                ? mapT('map_click_from', 'Кликните на карте — точка A (откуда)')
                : mapT('map_click_to', 'Кликните на карте — точка B (куда)');
        }
    }

    toggleSatellite() {
        this.satellite = !this.satellite;
        if (this.satellite) {
            this.map.removeLayer(this.layerDark);
            this.layerSatellite.addTo(this.map);
        } else {
            this.map.removeLayer(this.layerSatellite);
            this.layerDark.addTo(this.map);
        }
        this._satelliteBtn?.classList.toggle('active', this.satellite);
        document.getElementById('btnSatellite')?.classList.toggle('active', this.satellite);
    }

    clearFromMarker() {
        if (this.fromMarker) { this.map.removeLayer(this.fromMarker); this.fromMarker = null; }
        this.pickupPos = null;
        this._clearRouteLine();
    }

    clearToMarker() {
        if (this.toMarker) { this.map.removeLayer(this.toMarker); this.toMarker = null; }
        this.dropoffPos = null;
        this._clearRouteLine();
    }

    async _onClick(latlng) {
        const address = await reverseGeocode(latlng.lat, latlng.lng);
        if (this.clickTarget === 'from') {
            this._setPickup(latlng.lat, latlng.lng, address);
            this.onAddressUpdate('from', address);
            this.setClickTarget('to');
        } else {
            this._setDropoff(latlng.lat, latlng.lng, address);
            this.onAddressUpdate('to', address);
        }
        await this._buildRouteFromMarkers(false);
    }

    _setPickup(lat, lng, address) {
        this.pickupPos = { lat, lng, address };
        if (this.fromMarker) this.map.removeLayer(this.fromMarker);
        this.fromMarker = L.marker([lat, lng], {
            icon: markerIcon('A', false),
            draggable: !this.readOnly,
        }).addTo(this.map);
        if (!this.readOnly) {
            this.fromMarker.on('dragend', async () => {
                const p = this.fromMarker.getLatLng();
                const addr = await reverseGeocode(p.lat, p.lng);
                this.pickupPos = { lat: p.lat, lng: p.lng, address: addr };
                this.onAddressUpdate('from', addr);
                await this._buildRouteFromMarkers(false);
            });
        }
    }

    _setDropoff(lat, lng, address) {
        this.dropoffPos = { lat, lng, address };
        if (this.toMarker) this.map.removeLayer(this.toMarker);
        this.toMarker = L.marker([lat, lng], {
            icon: markerIcon('B', true),
            draggable: !this.readOnly,
        }).addTo(this.map);
        if (!this.readOnly) {
            this.toMarker.on('dragend', async () => {
                const p = this.toMarker.getLatLng();
                const addr = await reverseGeocode(p.lat, p.lng);
                this.dropoffPos = { lat: p.lat, lng: p.lng, address: addr };
                this.onAddressUpdate('to', addr);
                await this._buildRouteFromMarkers(false);
            });
        }
    }

    async setFromAddress(text) {
        const r = await geocodeAddress(text);
        if (!r) return false;
        this._setPickup(r.lat, r.lng, r.address);
        this.onAddressUpdate('from', r.address);
        return true;
    }

    async setToAddress(text) {
        const r = await geocodeAddress(text);
        if (!r) return false;
        this._setDropoff(r.lat, r.lng, r.address);
        this.onAddressUpdate('to', r.address);
        return true;
    }

    /** Строит маршрут: маркеры на карте имеют приоритет, текст — только если маркера нет */
    async buildRoute(fromText, toText) {
        if (!this.fromMarker && fromText?.trim()) await this.setFromAddress(fromText);
        if (!this.toMarker && toText?.trim()) await this.setToAddress(toText);
        return this._buildRouteFromMarkers(true);
    }

    async _buildRouteFromMarkers(adjustZoom) {
        const reqId = ++this._routeRequestId;

        if (!this.pickupPos || !this.dropoffPos) {
            this._clearRouteLine();
            this.onRouteUpdate(null);
            return null;
        }

        const route = await fetchRoute(this.pickupPos, this.dropoffPos);
        if (reqId !== this._routeRequestId) return null;

        if (!route) {
            this.onRouteUpdate(null);
            return null;
        }

        if (this.routeLine) this.map.removeLayer(this.routeLine);
        this.routeLine = L.polyline(route.coords, {
            color: '#ffffff', weight: 5, opacity: 0.9,
        }).addTo(this.map);

        if (adjustZoom) {
            this.map.fitBounds(this.routeLine.getBounds(), { padding: [80, 80], maxZoom: 14 });
        }

        this.routeData = {
            distanceKm: route.distanceKm,
            durationMin: route.durationMin,
            fromAddress: this.pickupPos.address,
            toAddress: this.dropoffPos.address,
        };
        this.onRouteUpdate(this.routeData);
        return this.routeData;
    }

    _clearRouteLine() {
        if (this.routeLine) { this.map.removeLayer(this.routeLine); this.routeLine = null; }
        this.routeData = null;
    }

    showCar(progress = 0.4) {
        if (!this.routeLine) return;
        const latlngs = this.routeLine.getLatLngs();
        const idx = Math.min(latlngs.length - 1, Math.max(0, Math.floor(latlngs.length * progress)));
        this.showCarAt(latlngs[idx].lat, latlngs[idx].lng);
    }

    showCarAt(lat, lng) {
        if (this.carMarker) this.map.removeLayer(this.carMarker);
        this.carMarker = L.marker([lat, lng], {
            icon: L.divIcon({ className: 'lf-car', html: '🚕', iconSize: [30, 30], iconAnchor: [15, 15] }),
        }).addTo(this.map);
    }

    _offsetPointKm(lat, lng, distKm, angleRad) {
        const dLat = (distKm / 111) * Math.cos(angleRad);
        const dLng = (distKm / (111 * Math.cos((lat * Math.PI) / 180))) * Math.sin(angleRad);
        return [lat + dLat, lng + dLng];
    }

    _haversineKm(lat1, lng1, lat2, lng2) {
        const toRad = (deg) => (deg * Math.PI) / 180;
        const dLat = toRad(lat2 - lat1);
        const dLng = toRad(lng2 - lng1);
        const a = Math.sin(dLat / 2) ** 2
            + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2;
        return 6371 * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    }

    /** Стартовая точка водителя рядом с A и подъезд по дорогам (OSRM), затем маршрут A→B */
    async prepareDriverPaths() {
        if (!this.pickupPos || !this.routeLine) {
            return { approachPath: [], tripPath: [], approachDurationMin: 3 };
        }

        const tripPath = this.routeLine.getLatLngs().map((p) => [p.lat, p.lng]);
        let approachPath = [];
        let approachDurationMin = 3;

        let biasAngle = null;
        if (tripPath.length >= 2) {
            const dLat = tripPath[0][0] - tripPath[1][0];
            const dLng = tripPath[0][1] - tripPath[1][1];
            biasAngle = Math.atan2(dLng, dLat);
        }

        for (let attempt = 0; attempt < 8; attempt += 1) {
            const angle = biasAngle !== null
                ? biasAngle + (Math.random() - 0.5) * Math.PI * 0.5
                : Math.random() * Math.PI * 2;
            const distKm = 0.3 + Math.random() * 0.55;
            const start = this._offsetPointKm(this.pickupPos.lat, this.pickupPos.lng, distKm, angle);
            const directKm = this._haversineKm(
                start[0], start[1], this.pickupPos.lat, this.pickupPos.lng,
            );

            const route = await fetchRoute(
                { lat: start[0], lng: start[1] },
                this.pickupPos,
            );
            if (!route?.coords?.length) continue;
            if (route.distanceKm > Math.max(1.8, directKm * 2.5)) continue;

            approachPath = route.coords;
            approachDurationMin = Math.max(1, route.durationMin || 2);
            break;
        }

        if (!approachPath.length && biasAngle !== null) {
            for (let i = 0; i < 4; i += 1) {
                const distKm = 0.25 + Math.random() * 0.35;
                const start = this._offsetPointKm(
                    this.pickupPos.lat, this.pickupPos.lng, distKm, biasAngle,
                );
                const route = await fetchRoute({ lat: start[0], lng: start[1] }, this.pickupPos);
                if (route?.coords?.length) {
                    approachPath = route.coords;
                    approachDurationMin = Math.max(1, route.durationMin || 2);
                    break;
                }
            }
        }

        this.approachPath = approachPath;
        this.tripPath = tripPath;
        this.approachDurationMin = approachDurationMin;
        return { approachPath, tripPath, approachDurationMin };
    }

    showApproachLine(path) {
        if (this.approachLine) this.map.removeLayer(this.approachLine);
        if (!path?.length) return;
        this.approachLine = L.polyline(path, {
            color: '#888',
            weight: 3,
            opacity: 0.55,
            dashArray: '8, 10',
        }).addTo(this.map);
    }

    _positionCarOnPath(path, progress) {
        if (!path?.length) return;
        const idx = Math.min(path.length - 1, Math.max(0, Math.floor(path.length * progress)));
        this.showCarAt(path[idx][0], path[idx][1]);
    }

    startContinuousCarOnPath(getProgress, shouldRun) {
        this.stopCarAnimation();
        const step = () => {
            if (!shouldRun()) return;
            const p = getProgress();
            if (p !== null) this._positionCarOnPath(this._activeCarPath, p);
            this._carAnimFrame = requestAnimationFrame(step);
        };
        this._carAnimFrame = requestAnimationFrame(step);
    }

    runCarOnPath(path, getProgress, shouldRun) {
        this._activeCarPath = path;
        this.startContinuousCarOnPath(getProgress, shouldRun);
    }

    animateCar(fromProgress, toProgress, durationMs = 4000, onDone) {
        if (!this.routeLine) return;
        this.stopCarAnimation();
        const start = performance.now();
        const step = (now) => {
            const t = Math.min(1, (now - start) / durationMs);
            const eased = 1 - Math.pow(1 - t, 3);
            const p = fromProgress + (toProgress - fromProgress) * eased;
            this.showCar(p);
            if (t < 1) {
                this._carAnimFrame = requestAnimationFrame(step);
            } else if (onDone) {
                onDone();
            }
        };
        this._carAnimFrame = requestAnimationFrame(step);
    }

    startContinuousCar(getProgress, shouldRun) {
        this.stopCarAnimation();
        const step = () => {
            if (!shouldRun()) return;
            const p = getProgress();
            if (p !== null) this.showCar(p);
            this._carAnimFrame = requestAnimationFrame(step);
        };
        this._carAnimFrame = requestAnimationFrame(step);
    }

    stopCarAnimation() {
        if (this._carAnimFrame) {
            cancelAnimationFrame(this._carAnimFrame);
            this._carAnimFrame = null;
        }
    }

    swapPoints() {
        if (!this.pickupPos || !this.dropoffPos) return null;
        const a = { ...this.pickupPos };
        const b = { ...this.dropoffPos };
        this._setPickup(b.lat, b.lng, b.address);
        this._setDropoff(a.lat, a.lng, a.address);
        this.onAddressUpdate('from', b.address);
        this.onAddressUpdate('to', a.address);
        return this._buildRouteFromMarkers(false);
    }

    _showUserLocation(lat, lng) {
        if (this.userCircle) this.map.removeLayer(this.userCircle);
        if (this.userMarker) this.map.removeLayer(this.userMarker);

        this.userCircle = L.circle([lat, lng], {
            radius: 80, color: '#ffffff', fillColor: '#ffffff',
            fillOpacity: 0.25, weight: 3,
        }).addTo(this.map);

        this.userMarker = L.marker([lat, lng], {
            icon: L.divIcon({
                className: 'lf-user-loc',
                html: '<div class="lf-user-dot"></div>',
                iconSize: [20, 20],
                iconAnchor: [10, 10],
            }),
        }).addTo(this.map);
    }

    locateUser(opts = {}) {
        const { setPickup = true, silent = false } = opts;
        if (!navigator.geolocation) {
            if (!silent) alert(mapT('map_geo_unavailable', 'Геолокация недоступна в браузере'));
            return;
        }

        const btns = [
            document.getElementById('locateBtn'),
            document.getElementById('panelLocateBtn'),
        ].filter(Boolean);

        btns.forEach((btn) => {
            btn.classList.add('loading');
            btn.disabled = true;
        });

        const finish = () => {
            btns.forEach((btn) => {
                btn.classList.remove('loading');
                btn.disabled = false;
            });
        };

        navigator.geolocation.getCurrentPosition(async (pos) => {
            const lat = pos.coords.latitude;
            const lng = pos.coords.longitude;
            this._showUserLocation(lat, lng);
            this.map.setView([lat, lng], 16, { animate: true });

            const address = await reverseGeocode(lat, lng);
            if (setPickup) {
                this._setPickup(lat, lng, address);
                this.onAddressUpdate('from', address);
                this.setClickTarget('to');
                const hint = document.getElementById('mapClickHint');
                if (hint) hint.textContent = mapT('map_hint_destination', 'Укажите пункт назначения на карте или в поле «Куда»');
            }

            finish();
            if (this.dropoffPos) {
                await this._buildRouteFromMarkers(false);
            }
        }, () => {
            finish();
            const hint = document.getElementById('mapClickHint');
            if (hint && silent) {
                hint.textContent = mapT('map_geo_manual', 'Разрешите геолокацию в браузере или укажите адрес вручную');
            } else if (!silent) {
                alert(mapT('map_geo_denied', 'Не удалось определить местоположение. Разрешите доступ к геолокации.'));
            }
        }, { enableHighAccuracy: true, timeout: 12000, maximumAge: 60000 });
    }
}

function createSimpleMap(elId, satellite = true) {
    const map = L.map(elId, { zoomControl: true, attributionControl: false }).setView(BERLIN, 11);
    (satellite ? L.tileLayer(TILES.satellite, { maxZoom: 19 }) : L.tileLayer(TILES.dark, { maxZoom: 19 })).addTo(map);
    setTimeout(() => map.invalidateSize(), 200);
    return map;
}

window.LeafletRideMap = LeafletRideMap;
window.createSimpleMap = createSimpleMap;
