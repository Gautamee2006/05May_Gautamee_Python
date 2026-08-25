# 🚕 CabGo — Modern Cab Booking Web Application

CabGo is a complete, modern, responsive cab booking web application built using **Django**, **HTML5/CSS3/JavaScript**, and **Google Maps JavaScript API**. It allows users to detect their current location, select pickup and drop points via Google Places Autocomplete or map clicks, calculate driving routes, distance, and estimated duration, compute dynamic fares across cab categories, book rides, view driver tracking details, and manage booking history.

---

## 🌟 Key Features

1. **📍 User Location Detection**: Instant browser HTML5 geolocation ("📍 Use My Location") with automatic map centering and reverse geocoding to readable addresses.
2. **🗺️ Google Maps Integration**: Custom dark-themed Google Map with Places Autocomplete, Geocoding API, Directions API route rendering, and interactive pin picking.
3. **🚕 Cab Category Selection**:
   - **Mini**: ₹10/km, 3 Passengers
   - **Sedan**: ₹15/km, 4 Passengers
   - **SUV**: ₹20/km, 6 Passengers
4. **💰 Dynamic Fare Engine**: Dynamic pricing formula: `Fare = Base Fare (₹50) + (Distance in KM × Per KM Rate)`. Realtime breakdown with double backend validation before saving.
5. **🛡️ Complete User Authentication**: Register, Login, Logout, session management, and protected ride booking routes.
6. **🧾 Confirmation & Real-time Simulation**: Interactive receipt screen featuring assigned driver details (Rahul Patel, Swift Dzire, ⭐ 4.8), driver contact, and simulated arrival tracker.
7. **📜 Booking History & Cancellation**: Full history at `/bookings/` with status filter tabs (*All*, *Confirmed*, *Completed*, *Cancelled*) and self-service ride cancellation.
8. **⚙️ Custom Django Admin**: Comprehensive management dashboard for viewing, searching, and updating ride statuses.
9. **🛡️ Intelligent Fallback Engine**: If a Google Maps API Key is not provided, CabGo seamlessly switches to an interactive map canvas with Haversine distance calculation so the app remains 100% operational under all environments.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.13+, Django 6.0, Django ORM, SQLite3
- **Frontend**: HTML5, CSS3 (Vanilla Glassmorphism styling), JavaScript (ES6+), Bootstrap 5, FontAwesome
- **APIs & Libraries**: Google Maps JavaScript API, Google Places Autocomplete, Google Geocoding API, Google Directions API, `python-dotenv`

---

## ⚙️ Setup & Installation

### 1. Clone & Navigate to Project Directory
```bash
cd cab-booking
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory (or copy `.env.example`):
```env
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
SECRET_KEY=your_django_secret_key
DEBUG=True
```
*Note: If `GOOGLE_MAPS_API_KEY` is left blank, CabGo will run in interactive Fallback Map Mode.*

### 4. Database Migrations
```bash
python manage.py makemigrations bookings
python manage.py migrate
```

### 5. Create Superuser (For Django Admin)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

Open your browser and visit: `http://127.0.0.1:8000/`

---

## 📁 Project Structure

```
cab-booking/
├── .env                     # Local environment settings (API keys & secrets)
├── .env.example             # Template environment configuration
├── .gitignore               # Excludes secrets, database, and bytecode
├── manage.py                # Django CLI entrypoint
├── requirements.txt         # Project dependencies
├── README.md                # Documentation
│
├── cab_booking/             # Core project configuration
│   ├── settings.py          # App configuration & dotenv loading
│   ├── urls.py              # Root routing table
│   ├── wsgi.py
│   └── asgi.py
│
└── bookings/                # Main Cab Booking App
    ├── admin.py             # Django Admin customization
    ├── context_processors.py# Injects Google Maps API key into templates
    ├── forms.py             # User Registration & Auth forms
    ├── models.py            # Booking ORM model & driver schema
    ├── urls.py              # URL routing
    ├── views.py             # Auth, Booking views & JSON API handlers
    ├── static/
    │   └── bookings/
    │       ├── css/
    │       │   └── style.css# Modern dark glassmorphic styling
    │       └── js/
    │           ├── maps.js  # Google Maps, Autocomplete, Geocoding, Directions & Fallback engine
    │           └── booking.js# Fare computation, cab selection & AJAX POST submission
    └── templates/
        └── bookings/
            ├── base.html         # Master template with navbar & footer
            ├── home.html         # Hero landing page & fleet showcase
            ├── book_cab.html     # Interactive 2-column cab booking panel
            ├── confirmation.html # Receipt, driver info & live simulation
            ├── bookings_list.html# Booking history & cancellation modal
            ├── login.html        # Authentication login page
            └── register.html     # User registration page
```

---

## 🔒 Security Best Practices

- Secret key and Google Maps API keys are isolated in `.env` and excluded via `.gitignore`.
- CSRF protection enabled on all POST endpoints (`X-CSRFToken` verification).
- Server-side validation of distances, locations, and fares prevents client-side price tampering.
- User ownership check ensures users can only view or cancel their own bookings.
