/**
 * CabGo - Booking Controller
 * Manages Cab Selection, Dynamic Fare Calculation, Form Validation, and AJAX Booking Submission.
 */

window.selectedCabRate = 15; // Default Sedan Rate ₹15/km
window.baseFare = 50;         // Default Base Fare ₹50

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupBookingEventListeners);
} else {
    setupBookingEventListeners();
}


function setupBookingEventListeners() {
    // Geolocation button
    const btnLocation = document.getElementById("btnUseMyLocation");
    if (btnLocation) {
        btnLocation.addEventListener("click", function() {
            if (window.detectUserLocation) {
                window.detectUserLocation(true);
            }
        });
    }

    // Book Cab Submission
    const btnBook = document.getElementById("btnBookCab");
    if (btnBook) {
        btnBook.addEventListener("click", submitCabBooking);
    }

    // Recenter Map
    const btnRecenter = document.getElementById("btnRecenterMap");
    if (btnRecenter) {
        btnRecenter.addEventListener("click", function() {
            const state = window.cabGoState;
            if (state.map && state.pickupLat) {
                state.map.panTo({ lat: state.pickupLat, lng: state.pickupLng });
                state.map.setZoom(14);
            }
        });
    }
}

/**
 * Handle Cab Selection Tab Click
 */
function selectCabType(cabName, ratePerKm, cardElement) {
    // Update active UI card
    const cards = document.querySelectorAll(".cab-card");
    cards.forEach(card => card.classList.remove("active"));
    cardElement.classList.add("active");

    // Update hidden field & state
    document.getElementById("selected_cab").value = cabName;
    window.selectedCabRate = parseFloat(ratePerKm);

    updateFareCalculation();
}
window.selectCabType = selectCabType;

/**
 * Dynamic Fare Calculation Formula
 * Fare = Base Fare (₹50) + (Distance in KM * Per KM Rate)
 */
function updateFareCalculation() {
    const distKm = window.cabGoState ? window.cabGoState.distanceKm : 0;
    const cabName = document.getElementById("selected_cab").value || "Sedan";
    const rate = window.selectedCabRate || 15;
    
    const base = window.baseFare || 50;
    let totalFare = 0;

    if (distKm > 0) {
        totalFare = Math.round(base + (distKm * rate));
    } else {
        totalFare = base;
    }

    // Update UI Labels
    const lblDist = document.getElementById("lblFareDistance");
    const lblType = document.getElementById("lblCabType");
    const lblRate = document.getElementById("lblFareRate");
    const lblTotal = document.getElementById("lblTotalFare");
    const metricFare = document.getElementById("metricFare");

    if (lblDist) lblDist.innerText = `${distKm} km`;
    if (lblType) lblType.innerText = cabName;
    if (lblRate) lblRate.innerText = `₹${rate}/km`;
    if (lblTotal) lblTotal.innerText = `₹${totalFare}`;
    if (metricFare) metricFare.innerText = `₹${totalFare}`;
}
window.updateFareCalculation = updateFareCalculation;

/**
 * AJAX Booking Submission
 */
function submitCabBooking() {
    const alertBox = document.getElementById("bookingAlert");
    alertBox.classList.add("d-none");

    const state = window.cabGoState || {};
    const pickupAddress = document.getElementById("pickupAddressInput").value.trim();
    const dropAddress = document.getElementById("dropAddressInput").value.trim();
    const pickupLat = document.getElementById("pickup_lat").value || state.pickupLat;
    const pickupLng = document.getElementById("pickup_lng").value || state.pickupLng;
    const dropLat = document.getElementById("drop_lat").value || state.dropLat;
    const dropLng = document.getElementById("drop_lng").value || state.dropLng;
    const distanceKm = parseFloat(document.getElementById("distance_km").value || state.distanceKm || 0);
    const estimatedTime = document.getElementById("estimated_time").value || state.estimatedTime || "15 min";
    const cabType = document.getElementById("selected_cab").value || "Sedan";
    const paymentMethod = document.getElementById("paymentMethod").value || "Cash";

    // Frontend Validations
    if (!pickupAddress || !pickupLat) {
        showBookingError("Please specify a valid Pickup Location.");
        return;
    }

    if (!dropAddress || !dropLat) {
        showBookingError("Please specify a valid Drop Destination.");
        return;
    }

    if (distanceKm <= 0) {
        showBookingError("Unable to calculate trip distance. Please re-select pickup and drop points.");
        return;
    }

    const payload = {
        pickup_address: pickupAddress,
        pickup_latitude: parseFloat(pickupLat),
        pickup_longitude: parseFloat(pickupLng),
        drop_address: dropAddress,
        drop_latitude: parseFloat(dropLat),
        drop_longitude: parseFloat(dropLng),
        distance_km: distanceKm,
        estimated_time: estimatedTime,
        cab_type: cabType,
        payment_method: paymentMethod
    };

    const btnBook = document.getElementById("btnBookCab");
    btnBook.disabled = true;
    btnBook.innerHTML = `<i class="fa-solid fa-spinner fa-spin me-2"></i> Confirming Booking...`;

    // Fetch CSRF Token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch("/api/bookings/create/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect_url;
        } else {
            showBookingError(data.error || "Booking failed. Please check inputs.");
            btnBook.disabled = false;
            btnBook.innerHTML = `<i class="fa-solid fa-taxi me-2"></i> Book Cab Now`;
        }
    })
    .catch(err => {
        console.error("Booking Error:", err);
        showBookingError("A network error occurred. Please try again.");
        btnBook.disabled = false;
        btnBook.innerHTML = `<i class="fa-solid fa-taxi me-2"></i> Book Cab Now`;
    });
}

function showBookingError(message) {
    const alertBox = document.getElementById("bookingAlert");
    if (alertBox) {
        alertBox.innerText = message;
        alertBox.classList.remove("d-none");
    }
}
