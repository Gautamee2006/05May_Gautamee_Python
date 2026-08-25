# QuickCart - Production-Style E-Commerce Platform

QuickCart is a full-featured, modular online shopping application built with **Python & Django**. It features an original, sleek custom design with Bootstrap 5, Font Awesome icons, interactive client JS, full order fulfillment tracking, coupon management, user authentication with OTP verification, and a dedicated admin/seller dashboard.

---

## 🌟 Key Features

1. **User Accounts & Authentication (`accounts`)**
   - User Registration with Email OTP Verification
   - Login, Logout, Profile Management with Profile Picture Upload
   - Multiple Saved Delivery Addresses (Home, Work, Other) with Default Flag
   - Recently Viewed Products tracking

2. **Catalog & Search (`products`)**
   - Categorized Product Browsing with Multi-Level Filters (Category, Price Range, Min Rating, Availability)
   - Dynamic Price Calculation (Auto-calculates discount & final price)
   - Search Functionality across name, brand, SKU, and description
   - Customer Product Reviews & Dynamic Rating updates

3. **Cart & Wishlist (`cart`)**
   - Session & User Persistent Cart with Live Subtotal, Product Discount, Delivery Charge, and Coupon Discount calculations
   - One-click Wishlist Toggle & "Move Wishlist to Cart" functionality
   - Stock Level Validation to prevent over-ordering

4. **Coupons & Promotional Offers (`coupons`)**
   - Percentage (%) and Fixed Amount (₹) Coupon Discounts
   - Expiry Date, Usage Limits, and Minimum Order Value Validation

5. **Checkout, Orders & Payments (`orders`, `payments`)**
   - Address Selection & Snapshotting (preserves address state at order placement)
   - Cash on Delivery (COD) and Online Payment Gateway Simulation
   - Order Status Lifecycle: `Placed` → `Confirmed` → `Packed` → `Shipped` → `Out for Delivery` → `Delivered` → `Cancelled` / `Returned`
   - Visual Stepper Tracking Timeline for Order Status
   - Order Cancellation & Product Return Requests
   - Printable HTML Invoices

6. **Customer Support & Notifications (`support`, `notifications`)**
   - Categorized Expandable FAQs Accordion
   - Support Ticket System (Open, In Progress, Resolved, Closed)
   - Real-time Notifications with Unread Counters

7. **Admin & Seller Dashboard (`dashboard`)**
   - Real-time KPI Statistics (Total Revenue, Orders, Users, Low Stock Alerts)
   - Interactive Chart.js Order Status Visualizer
   - Product & Category CRUD Operations
   - Inventory Management & Direct Stock Updates
   - Order Status Transition Controls
   - User Account Activation/Deactivation
   - Support Ticket Status Controls

---

## 📁 Project Architecture

```
quickcart/
│
├── manage.py
├── seed_data.py
├── requirements.txt
├── README.md
│
├── quickcart/                 # Project Configuration & Context Processors
│   ├── settings.py
│   ├── urls.py
│   ├── context_processors.py  # Site-wide context variables
│   └── wsgi.py
│
├── accounts/                  # User Profiles, Addresses, OTP & Recently Viewed
├── products/                  # Product Catalog, Categories, Images & Reviews
├── cart/                      # Cart Items & Wishlist Management
├── coupons/                   # Coupon Code Engine
├── orders/                    # Checkout, Order Lifecycle & Invoices
├── payments/                  # Payment Gateway Simulation
├── notifications/             # In-App Notifications
├── support/                   # Support Tickets & FAQs
├── dashboard/                 # Admin & Seller Panel
│
├── static/                    # Custom CSS, JS, and Media Assets
│   ├── css/style.css
│   └── js/script.js
│
└── templates/                 # Modular HTML Templates
    ├── base.html
    ├── home.html
    ├── accounts/
    ├── products/
    ├── cart/
    ├── orders/
    ├── payments/
    ├── coupons/
    ├── support/
    ├── notifications/
    └── dashboard/
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ installed
- Virtual environment (recommended)

### 2. Installation & Setup
```bash
# Navigate to project directory
cd quickcart

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Seed sample data (Admin account, categories, products, coupons, FAQs)
python seed_data.py
```

### 3. Run Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## 🔑 Demo Login Credentials

- **Admin / Staff Dashboard**:
  - **Username**: `admin`
  - **Password**: `admin123`
  - **Dashboard URL**: `http://127.0.0.1:8000/dashboard/`

- **Customer Account**:
  - **Username**: `john_doe`
  - **Password**: `pass123`
