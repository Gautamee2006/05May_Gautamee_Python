/**
 * CabGo - Google Maps & OpenStreetMap Location Engine
 * Dual Map Engine: Google Maps API SDK (Primary) + Leaflet/OpenStreetMap (Zero-Config Live Fallback Engine)
 */

// Global State
window.cabGoState = {
    map: null,
    pickupMarker: null,
    dropMarker: null,
    nearbyMarkers: [],
    directionsService: null,
    directionsRenderer: null,
    geocoder: null,
    pickupLat: null,
    pickupLng: null,
    pickupAddress: '',
    dropLat: null,
    dropLng: null,
    dropAddress: '',
    distanceKm: 0,
    estimatedTime: '0 min',
    isGoogleLoaded: false,
    isLeaflet: false,
    leafletMap: null,
    leafletTileLayer: null,
    leafletPickupMarker: null,
    leafletDropMarker: null,
    leafletPolyline: null,
    clickTarget: 'pickup' // 'pickup' or 'drop'
};

// Default fallback coordinates (Rajkot, Gujarat)
const DEFAULT_LAT = 22.3039;
const DEFAULT_LNG = 70.8022;

// DOM Ready Guard preventing race conditions
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initMapEngine);
} else {
    initMapEngine();
}

function initMapEngine() {
    const apiKey = window.GOOGLE_MAPS_API_KEY;
    
    if (apiKey && apiKey.trim() !== "" && apiKey !== "YOUR_GOOGLE_MAPS_API_KEY") {
        console.log("Loading Google Maps API SDK...");
        loadGoogleMapsScript(apiKey);
    } else {
        console.warn("No Google Maps API Key provided. Initializing Live Leaflet / OpenStreetMap Engine.");
        initCabGoLeafletMap();
    }
}

function loadGoogleMapsScript(apiKey) {
    window.initCabGoMap = initCabGoMap;
    
    if (document.getElementById("googleMapsScript")) return;

    const script = document.createElement("script");
    script.id = "googleMapsScript";
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places&callback=initCabGoMap`;
    script.async = true;
    script.defer = true;
    script.onerror = function() {
        console.error("Google Maps Script failed to load. Switching to Leaflet OpenStreetMap.");
        initCabGoLeafletMap();
    };
    document.head.appendChild(script);

    window.gm_authFailure = function() {
        console.error("Google Maps Auth Failure. Switching to Leaflet OpenStreetMap.");
        initCabGoLeafletMap();
    };
}

/**
 * Primary Google Maps Initializer
 */
function initCabGoMap() {
    window.cabGoState.isGoogleLoaded = true;
    const mapElement = document.getElementById("map");
    if (!mapElement) return;

    const badge = document.getElementById("mapStatusBadge");
    if (badge) {
        badge.innerHTML = `<i class="fa-solid fa-circle-check text-success me-1"></i> Google Maps Active`;
    }

    const activeTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const mapOptions = {
        center: { lat: DEFAULT_LAT, lng: DEFAULT_LNG },
        zoom: 13,
        styles: activeTheme === 'light' ? [] : getDarkMapStyles(),
        mapTypeControl: false,
        streetViewControl: false,
        fullscreenControl: true
    };

    const state = window.cabGoState;
    state.map = new google.maps.Map(mapElement, mapOptions);
    state.geocoder = new google.maps.Geocoder();
    state.directionsService = new google.maps.DirectionsService();
    state.directionsRenderer = new google.maps.DirectionsRenderer({
        map: state.map,
        suppressMarkers: true,
        polylineOptions: {
            strokeColor: "#ffb703",
            strokeWeight: 6,
            strokeOpacity: 0.8
        }
    });

    state.pickupMarker = new google.maps.Marker({
        map: state.map,
        icon: {
            url: "https://maps.google.com/mapfiles/ms/icons/green-dot.png",
            scaledSize: new google.maps.Size(42, 42)
        },
        draggable: true,
        title: "Pickup Location"
    });

    state.dropMarker = new google.maps.Marker({
        map: state.map,
        icon: {
            url: "https://maps.google.com/mapfiles/ms/icons/red-dot.png",
            scaledSize: new google.maps.Size(42, 42)
        },
        draggable: true,
        title: "Drop Location"
    });

    setupGooglePlacesAutocomplete();

    state.map.addListener("click", function(e) {
        handleMapClick(e.latLng.lat(), e.latLng.lng());
    });

    state.pickupMarker.addListener("dragend", function(e) {
        setPickupLocation(e.latLng.lat(), e.latLng.lng(), true);
    });

    state.dropMarker.addListener("dragend", function(e) {
        setDropLocation(e.latLng.lat(), e.latLng.lng(), true);
    });

    detectUserLocation(false);
    renderSimulatedNearbyCabs(DEFAULT_LAT, DEFAULT_LNG);
}

/**
 * Leaflet & OpenStreetMap Live Engine (Zero-Config Fallback)
 */
function initCabGoLeafletMap() {
    const mapElement = document.getElementById("map");
    if (!mapElement) return;

    if (typeof L === "undefined") {
        console.warn("Leaflet library not loaded. Falling back to canvas mode.");
        initCanvasFallbackMap();
        return;
    }

    mapElement.innerHTML = "";

    const badge = document.getElementById("mapStatusBadge");
    if (badge) {
        badge.innerHTML = `<i class="fa-solid fa-map-location-dot text-success me-1"></i> Live Map Active (OpenStreetMap)`;
    }

    const state = window.cabGoState;
    state.isLeaflet = true;

    state.leafletMap = L.map("map").setView([DEFAULT_LAT, DEFAULT_LNG], 13);

    const activeTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    updateLeafletTileLayer(activeTheme);

    const pickupIcon = L.divIcon({
        className: 'leaflet-custom-marker',
        html: '<div style="background:#10b981; color:#ffffff; width:34px; height:34px; border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 12px rgba(16,185,129,0.6); font-size:16px; border:2px solid #ffffff;"><i class="fa-solid fa-location-dot"></i></div>',
        iconSize: [34, 34],
        iconAnchor: [17, 34]
    });

    const dropIcon = L.divIcon({
        className: 'leaflet-custom-marker',
        html: '<div style="background:#ef4444; color:#ffffff; width:34px; height:34px; border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 12px rgba(239,68,68,0.6); font-size:16px; border:2px solid #ffffff;"><i class="fa-solid fa-flag-checkered"></i></div>',
        iconSize: [34, 34],
        iconAnchor: [17, 34]
    });

    state.pickupIcon = pickupIcon;
    state.dropIcon = dropIcon;

    state.leafletMap.on("click", function(e) {
        handleMapClick(e.latlng.lat, e.latlng.lng);
    });

    detectUserLocation(false);
}

function updateLeafletTileLayer(theme) {
    const state = window.cabGoState;
    if (!state.leafletMap) return;

    if (state.leafletTileLayer) {
        state.leafletMap.removeLayer(state.leafletTileLayer);
    }

    const tileUrl = theme === 'light'
        ? 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
        : 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png';

    state.leafletTileLayer = L.tileLayer(tileUrl, {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(state.leafletMap);
}

/**
 * Google Places Autocomplete Configuration
 */
function setupGooglePlacesAutocomplete() {
    const pickupInput = document.getElementById("pickupAddressInput");
    const dropInput = document.getElementById("dropAddressInput");

    if (pickupInput && window.google && google.maps && google.maps.places) {
        const pAutocomplete = new google.maps.places.Autocomplete(pickupInput);
        pAutocomplete.addListener("place_changed", function() {
            const place = pAutocomplete.getPlace();
            if (place.geometry && place.geometry.location) {
                setPickupLocation(place.geometry.location.lat(), place.geometry.location.lng(), false, place.formatted_address || place.name);
            }
        });
    }

    if (dropInput && window.google && google.maps && google.maps.places) {
        const dAutocomplete = new google.maps.places.Autocomplete(dropInput);
        dAutocomplete.addListener("place_changed", function() {
            const place = dAutocomplete.getPlace();
            if (place.geometry && place.geometry.location) {
                setDropLocation(place.geometry.location.lat(), place.geometry.location.lng(), false, place.formatted_address || place.name);
            }
        });
    }
}

/**
 * Handle Map Click Interaction
 */
function handleMapClick(lat, lng) {
    const state = window.cabGoState;
    if (!state.pickupLat) {
        setPickupLocation(lat, lng, true);
        state.clickTarget = "drop";
    } else if (!state.dropLat) {
        setDropLocation(lat, lng, true);
        state.clickTarget = "pickup";
    } else {
        if (state.clickTarget === "pickup") {
            setPickupLocation(lat, lng, true);
            state.clickTarget = "drop";
        } else {
            setDropLocation(lat, lng, true);
            state.clickTarget = "pickup";
        }
    }
    updatePinModeText();
}

function updatePinModeText() {
    const textEl = document.getElementById("pinModeText");
    if (textEl) {
        textEl.innerText = `Click Map sets: ${window.cabGoState.clickTarget.toUpperCase()}`;
    }
}

/**
 * Set Pickup Location
 */
function setPickupLocation(lat, lng, fetchAddress = true, addressString = "") {
    const state = window.cabGoState;
    state.pickupLat = lat;
    state.pickupLng = lng;

    const pLat = document.getElementById("pickup_lat");
    const pLng = document.getElementById("pickup_lng");
    if (pLat) pLat.value = lat;
    if (pLng) pLng.value = lng;

    // Google Maps Marker
    if (state.isGoogleLoaded && state.pickupMarker) {
        state.pickupMarker.setPosition({ lat, lng });
        state.pickupMarker.setVisible(true);
        state.map.panTo({ lat, lng });
    }

    // Leaflet Marker
    if (state.isLeaflet && state.leafletMap) {
        if (!state.leafletPickupMarker) {
            state.leafletPickupMarker = L.marker([lat, lng], { icon: state.pickupIcon, draggable: true }).addTo(state.leafletMap);
            state.leafletPickupMarker.on("dragend", function(e) {
                const coord = e.target.getLatLng();
                setPickupLocation(coord.lat, coord.lng, true);
            });
        } else {
            state.leafletPickupMarker.setLatLng([lat, lng]);
        }
        state.leafletMap.panTo([lat, lng]);
    }

    // Geocoding
    if (fetchAddress) {
        if (state.isGoogleLoaded && state.geocoder) {
            state.geocoder.geocode({ location: { lat, lng } }, function(results, status) {
                if (status === "OK" && results[0]) {
                    updatePickupAddressUI(results[0].formatted_address);
                } else {
                    updatePickupAddressUI(`Pickup Point (${lat.toFixed(4)}, ${lng.toFixed(4)})`);
                }
            });
        } else {
            // Leaflet Nominatim Geocoding
            fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`)
                .then(res => res.json())
                .then(data => {
                    if (data && data.display_name) {
                        const parts = data.display_name.split(',');
                        updatePickupAddressUI(parts.slice(0, 3).join(','));
                    } else {
                        updatePickupAddressUI(`Pickup Point (${lat.toFixed(4)}, ${lng.toFixed(4)})`);
                    }
                })
                .catch(() => updatePickupAddressUI(`Pickup Point (${lat.toFixed(4)}, ${lng.toFixed(4)})`));
        }
    } else if (addressString) {
        updatePickupAddressUI(addressString);
    } else {
        updatePickupAddressUI(`Pickup Point (${lat.toFixed(4)}, ${lng.toFixed(4)})`);
    }

    calculateRoute();
}

/**
 * Set Drop Location
 */
function setDropLocation(lat, lng, fetchAddress = true, addressString = "") {
    const state = window.cabGoState;
    state.dropLat = lat;
    state.dropLng = lng;

    const dLat = document.getElementById("drop_lat");
    const dLng = document.getElementById("drop_lng");
    if (dLat) dLat.value = lat;
    if (dLng) dLng.value = lng;

    // Google Maps Marker
    if (state.isGoogleLoaded && state.dropMarker) {
        state.dropMarker.setPosition({ lat, lng });
        state.dropMarker.setVisible(true);
    }

    // Leaflet Marker
    if (state.isLeaflet && state.leafletMap) {
        if (!state.leafletDropMarker) {
            state.leafletDropMarker = L.marker([lat, lng], { icon: state.dropIcon, draggable: true }).addTo(state.leafletMap);
            state.leafletDropMarker.on("dragend", function(e) {
                const coord = e.target.getLatLng();
                setDropLocation(coord.lat, coord.lng, true);
            });
        } else {
            state.leafletDropMarker.setLatLng([lat, lng]);
        }
    }

    // Geocoding
    if (fetchAddress) {
        if (state.isGoogleLoaded && state.geocoder) {
            state.geocoder.geocode({ location: { lat, lng } }, function(results, status) {
                if (status === "OK" && results[0]) {
                    updateDropAddressUI(results[0].formatted_address);
                } else {
                    updateDropAddressUI(`Destination (${lat.toFixed(4)}, ${lng.toFixed(4)})`);
                }
            });
        } else {
            // Leaflet Nominatim Geocoding
            fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`)
                .then(res => res.json())
                .then(data => {
                    if (data && data.display_name) {
                        const parts = data.display_name.split(',');
                        updateDropAddressUI(parts.slice(0, 3).join(','));
                    } else {
                        updateDropAddressUI(`Destination (${lat.toFixed(4)}, ${lng.toFixed(4)})`);
                    }
                })
                .catch(() => updateDropAddressUI(`Destination (${lat.toFixed(4)}, ${lng.toFixed(4)})`));
        }
    } else if (addressString) {
        updateDropAddressUI(addressString);
    } else {
        updateDropAddressUI(`Destination (${lat.toFixed(4)}, ${lng.toFixed(4)})`);
    }

    calculateRoute();
}

function updatePickupAddressUI(address) {
    window.cabGoState.pickupAddress = address;
    const lbl = document.getElementById("lblPickupAddress");
    const input = document.getElementById("pickupAddressInput");
    if (lbl) lbl.innerText = address;
    if (input) input.value = address;
}

function updateDropAddressUI(address) {
    window.cabGoState.dropAddress = address;
    const lbl = document.getElementById("lblDropAddress");
    const input = document.getElementById("dropAddressInput");
    if (lbl) lbl.innerText = address;
    if (input) input.value = address;
}

/**
 * Calculate Route & Distance
 */
function calculateRoute() {
    const state = window.cabGoState;
    if (!state.pickupLat || !state.dropLat) return;

    if (state.isGoogleLoaded && state.directionsService) {
        state.directionsService.route(
            {
                origin: { lat: state.pickupLat, lng: state.pickupLng },
                destination: { lat: state.dropLat, lng: state.dropLng },
                travelMode: google.maps.TravelMode.DRIVING
            },
            function(response, status) {
                if (status === "OK" && response.routes[0]) {
                    state.directionsRenderer.setDirections(response);
                    const leg = response.routes[0].legs[0];
                    const distKm = (leg.distance.value / 1000).toFixed(1);
                    updateRouteMetrics(distKm, leg.duration.text);
                } else {
                    fallbackRouteMetrics();
                }
            }
        );
    } else if (state.isLeaflet && state.leafletMap) {
        // Draw polyline on Leaflet
        if (state.leafletPolyline) {
            state.leafletMap.removeLayer(state.leafletPolyline);
        }
        state.leafletPolyline = L.polyline([
            [state.pickupLat, state.pickupLng],
            [state.dropLat, state.dropLng]
        ], { color: '#ffb703', weight: 5, dashArray: '8, 8' }).addTo(state.leafletMap);

        state.leafletMap.fitBounds(state.leafletPolyline.getBounds(), { padding: [50, 50] });

        fallbackRouteMetrics();
    } else {
        fallbackRouteMetrics();
    }
}

function fallbackRouteMetrics() {
    const state = window.cabGoState;
    if (!state.pickupLat || !state.dropLat) return;

    const distKm = calculateHaversineDistance(
        state.pickupLat, state.pickupLng,
        state.dropLat, state.dropLng
    ).toFixed(1);

    const estMinutes = Math.round(distKm * 2.5) + 3;
    updateRouteMetrics(distKm, `${estMinutes} mins`);
}

function updateRouteMetrics(distKm, timeText) {
    const state = window.cabGoState;
    state.distanceKm = parseFloat(distKm);
    state.estimatedTime = timeText;

    const dInput = document.getElementById("distance_km");
    const tInput = document.getElementById("estimated_time");
    const mDist = document.getElementById("metricDistance");
    const mTime = document.getElementById("metricTime");
    const lDist = document.getElementById("lblFareDistance");

    if (dInput) dInput.value = distKm;
    if (tInput) tInput.value = timeText;
    if (mDist) mDist.innerText = `${distKm} km`;
    if (mTime) mTime.innerText = timeText;
    if (lDist) lDist.innerText = `${distKm} km`;

    if (window.updateFareCalculation) {
        window.updateFareCalculation();
    }
}

function calculateHaversineDistance(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
}

/**
 * Browser Geolocation API ("📍 Use My Location")
 */
function detectUserLocation(showAlerts = true) {
    const btn = document.getElementById("btnUseMyLocation");
    if (btn) btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin me-1"></i> Locating...`;

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                setPickupLocation(lat, lng, true);
                if (btn) btn.innerHTML = `<i class="fa-solid fa-location-crosshairs me-1"></i> Use My Location`;
            },
            function(error) {
                if (btn) btn.innerHTML = `<i class="fa-solid fa-location-crosshairs me-1"></i> Use My Location`;
                if (showAlerts) alert("Location permission denied or timed out.");
                setPickupLocation(DEFAULT_LAT, DEFAULT_LNG, false, "Rajkot Station, Gujarat");
            },
            { timeout: 10000, enableHighAccuracy: true }
        );
    } else {
        if (btn) btn.innerHTML = `<i class="fa-solid fa-location-crosshairs me-1"></i> Use My Location`;
        if (showAlerts) alert("Geolocation not supported.");
        setPickupLocation(DEFAULT_LAT, DEFAULT_LNG, false, "Rajkot Station, Gujarat");
    }
}

function renderSimulatedNearbyCabs(centerLat, centerLng) {
    const state = window.cabGoState;
    if (!state.isGoogleLoaded || !state.map) return;

    const cabIcon = {
        url: "https://cdn-icons-png.flaticon.com/512/1048/1048313.png",
        scaledSize: new google.maps.Size(28, 28)
    };

    const offsets = [
        { lat: 0.008, lng: 0.006 },
        { lat: -0.007, lng: 0.009 },
        { lat: 0.005, lng: -0.008 },
        { lat: -0.009, lng: -0.005 }
    ];

    offsets.forEach(offset => {
        const marker = new google.maps.Marker({
            position: { lat: centerLat + offset.lat, lng: centerLng + offset.lng },
            map: state.map,
            icon: cabIcon,
            title: "CabGo Nearby Cab"
        });
        state.nearbyMarkers.push(marker);
    });
}

function getDarkMapStyles() {
    return [
        { "elementType": "geometry", "stylers": [{ "color": "#1d2c4d" }] },
        { "elementType": "labels.text.fill", "stylers": [{ "color": "#8ec3b9" }] },
        { "elementType": "labels.text.stroke", "stylers": [{ "color": "#1a3646" }] },
        { "featureType": "administrative.country", "elementType": "geometry.stroke", "stylers": [{ "color": "#4b687a" }] },
        { "featureType": "road", "elementType": "geometry", "stylers": [{ "color": "#304a7d" }] },
        { "featureType": "road", "elementType": "geometry.stroke", "stylers": [{ "color": "#1f2835" }] },
        { "featureType": "road.highway", "elementType": "geometry", "stylers": [{ "color": "#2c4568" }] },
        { "featureType": "water", "elementType": "geometry", "stylers": [{ "color": "#0e1626" }] }
    ];
}

function updateMapTheme(theme) {
    const state = window.cabGoState;
    if (state.isGoogleLoaded && state.map) {
        state.map.setOptions({ styles: theme === 'light' ? [] : getDarkMapStyles() });
    } else if (state.isLeaflet && state.leafletMap) {
        updateLeafletTileLayer(theme);
    }
}
window.updateMapTheme = updateMapTheme;
