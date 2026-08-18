# Food Delivery REST API Backend

A fully functional, clean, and beginner-friendly Food Delivery REST API backend built using **Python**, **Django**, and **Django REST Framework (DRF)** with **SQLite**.

---

## Objective

The objective of this project is to provide a complete REST API backend for a Food Delivery system. It exposes full CRUD capabilities for **Categories**, **Menu Items**, and **Orders** using DRF's `ModelSerializer`, `ModelViewSet`, and `DefaultRouter`, complete with **Token Authentication**, **Pagination**, **Filtering**, and **Custom Validation Logic**.

---

## Features

- **Category Management API**: Public CRUD operations for food categories.
- **Menu Item Management API**: Public CRUD operations for menu items with price validation.
- **Order Processing API**: Protected order creation auto-linked to `request.user`.
- **User Order History (`/api/my-orders/`)**: Protected endpoint displaying only the logged-in user's orders.
- **Token Authentication (`/api-token-auth/`)**: Secure token generation using `rest_framework.authtoken`.
- **Status Filtering**: Filter orders dynamically via query parameter (`?status=pending|confirmed|delivered`).
- **Pagination**: Built-in PageNumberPagination configured to 5 items per page (`PAGE_SIZE = 5`).
- **Django Admin Integration**: Fully configured models registered in Django Admin panel.

---

## Technologies Used

- **Python**: 3.10+
- **Django**: 6.0+
- **Django REST Framework**: 3.18+
- **Database**: SQLite3
- **Authentication**: DRF TokenAuthentication (`rest_framework.authtoken`)

---

## Installation Steps

1. **Navigate to the Project Directory**:
   ```bash
   cd food_delivery
   ```

2. **Install Dependencies** (if not already installed):
   ```bash
   pip install django djangorestframework
   ```

3. **Apply Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Seed Sample Data (Users, Categories, Menu Items, Orders, Tokens)**:
   ```bash
   python manage.py seed_data
   ```

5. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://127.0.0.1:8000/`.

---

## Project Structure

```
food_delivery/
│
├── manage.py
├── test_api.py
├── db.sqlite3
├── README.md
│
├── docs/
│   └── screenshots/
│       └── README.md
│
├── food_delivery/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── food_api/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── management/
    │   └── commands/
    │       ├── __init__.py
    │       └── seed_data.py
    └── migrations/
        ├── 0001_initial.py
        └── __init__.py
```

---

## Database Models

### 1. Category Model
- `id`: Auto-generated Primary Key.
- `name`: CharField (max_length=100) - Category name.
- `description`: TextField - Category details.

### 2. MenuItem Model
- `id`: Auto-generated Primary Key.
- `name`: CharField (max_length=100) - Dish name.
- `price`: DecimalField (max_digits=10, decimal_places=2) - Price in INR.
- `category`: ForeignKey to `Category` (on_delete=CASCADE, related_name='menu_items').
- `is_available`: BooleanField (default=True) - Item availability status.

### 3. Order Model
- `id`: Auto-generated Primary Key.
- `customer`: ForeignKey to Django built-in `User` (on_delete=CASCADE, related_name='orders').
- `item`: CharField (max_length=100) - Ordered dish name.
- `quantity`: IntegerField - Number of items.
- `status`: CharField choices (`pending`, `confirmed`, `delivered`), default=`pending`.
- `created_at`: DateTimeField (auto_now_add=True) - Creation timestamp.

---

## Serializer Details

All serializers inherit from `rest_framework.serializers.ModelSerializer`:

1. **CategorySerializer**:
   - Fields: `['id', 'name', 'description']`
   - Validates `name`: Cannot be empty or contain only whitespace. Raises `"Category name cannot be empty."`
2. **MenuItemSerializer**:
   - Fields: `['id', 'name', 'price', 'category', 'is_available']`
   - Validates `name`: Cannot be empty or whitespace. Raises `"Menu item name cannot be empty."`
   - Validates `price`: Must be greater than 0 (`price > 0`). Raises `"Price must be greater than 0."`
3. **OrderSerializer**:
   - Fields: `['id', 'customer', 'item', 'quantity', 'status', 'created_at']`
   - `customer` is marked `read_only=True` (auto-assigned from `request.user`).
   - Validates `item`: Cannot be empty. Raises `"Item name cannot be empty."`
   - Validates `quantity`: Must be `>= 1`. Raises `"Quantity must be at least 1."`
   - Validates `status`: Must be one of `pending`, `confirmed`, or `delivered`.

---

## API Endpoint Table

| Method | Endpoint | Purpose | Authentication | Expected Status Code |
|--------|----------|---------|----------------|----------------------|
| **GET** | `/api/categories/` | List all food categories | None (Public) | `200 OK` |
| **POST** | `/api/categories/` | Create a new category | None (Public) | `201 Created` |
| **GET** | `/api/categories/<id>/` | Get category details | None (Public) | `200 OK` |
| **PUT** | `/api/categories/<id>/` | Update a category | None (Public) | `200 OK` |
| **PATCH** | `/api/categories/<id>/` | Partial update category | None (Public) | `200 OK` |
| **DELETE** | `/api/categories/<id>/` | Delete a category | None (Public) | `204 No Content` |
| **GET** | `/api/menu-items/` | List all menu items | None (Public) | `200 OK` |
| **POST** | `/api/menu-items/` | Create a menu item | None (Public) | `201 Created` |
| **GET** | `/api/menu-items/<id>/` | Get menu item details | None (Public) | `200 OK` |
| **PUT** | `/api/menu-items/<id>/` | Update a menu item | None (Public) | `200 OK` |
| **PATCH** | `/api/menu-items/<id>/` | Partial update menu item | None (Public) | `200 OK` |
| **DELETE** | `/api/menu-items/<id>/` | Delete a menu item | None (Public) | `204 No Content` |
| **GET** | `/api/orders/` | List all orders (Paginated) | None (Public) | `200 OK` |
| **POST** | `/api/orders/` | Create an order | Token Authentication | `201 Created` |
| **GET** | `/api/orders/<id>/` | Get order details | None (Public) | `200 OK` |
| **PUT** | `/api/orders/<id>/` | Update an order | Token Authentication | `200 OK` |
| **PATCH** | `/api/orders/<id>/` | Partial update order | Token Authentication | `200 OK` |
| **DELETE** | `/api/orders/<id>/` | Delete an order | Token Authentication | `204 No Content` |
| **GET** | `/api/my-orders/` | Get logged-in user order history | Token Authentication | `200 OK` |
| **POST** | `/api-token-auth/` | Obtain token for authentication | None (Public) | `200 OK` |

---

## Authentication Instructions

The API uses **DRF TokenAuthentication**.

1. **Obtain Token**: Send a POST request to `/api-token-auth/` with `username` and `password`.
   ```json
   {
       "username": "testuser",
       "password": "testpassword"
   }
   ```
   **Response**:
   ```json
   {
       "token": "487c2113cd61d046d733b1d5a3f45017aab432e1"
   }
   ```

2. **Use Token in Headers**: Include the `Authorization` header in all protected requests:
   ```http
   Authorization: Token 487c2113cd61d046d733b1d5a3f45017aab432e1
   ```

---

## Pagination Instructions

The API uses `PageNumberPagination` with `PAGE_SIZE = 5`.

- **Page 1**: `GET http://127.0.0.1:8000/api/orders/?page=1`
- **Page 2**: `GET http://127.0.0.1:8000/api/orders/?page=2`

Response structure:
```json
{
    "count": 8,
    "next": "http://127.0.0.1:8000/api/orders/?page=2",
    "previous": null,
    "results": [ ... ]
}
```

---

## Filtering Instructions

Filter orders by status using the `status` query parameter:

- **Pending Orders**: `GET http://127.0.0.1:8000/api/orders/?status=pending`
- **Confirmed Orders**: `GET http://127.0.0.1:8000/api/orders/?status=confirmed`
- **Delivered Orders**: `GET http://127.0.0.1:8000/api/orders/?status=delivered`

---

## Validation Rules

1. **Category Name**: Cannot be blank or empty.
   - Error Response: `400 Bad Request` -> `{"name": ["Category name cannot be empty."]}`
2. **MenuItem Name & Price**:
   - `name`: Cannot be empty.
   - `price`: Must be greater than 0 (`price > 0`).
   - Error Response: `400 Bad Request` -> `{"price": ["Price must be greater than 0."]}`
3. **Order Quantity**: Must be greater than or equal to 1 (`quantity >= 1`).
   - Error Response: `400 Bad Request` -> `{"quantity": ["Quantity must be at least 1."]}`

---

## How to Create Superuser

Run the following command and follow the prompts:
```bash
python manage.py createsuperuser
```

---

## How to Run Server

```bash
python manage.py runserver
```

Open Django Admin at `http://127.0.0.1:8000/admin/`.

---

## Postman Testing Instructions

### 1. GET Categories
- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/api/categories/`
- **Expected Status**: `200 OK`

### 2. POST Category
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/api/categories/`
- **Body** (JSON):
  ```json
  {
      "name": "Desserts",
      "description": "Sweet food items"
  }
  ```
- **Expected Status**: `201 Created`

### 3. GET Menu Items
- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/api/menu-items/`
- **Expected Status**: `200 OK`

### 4. POST Menu Item
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/api/menu-items/`
- **Body** (JSON):
  ```json
  {
      "name": "Margherita Pizza",
      "price": 250,
      "category": 1,
      "is_available": true
  }
  ```
- **Expected Status**: `201 Created`

### 5. Test Invalid Price (Validation Error)
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/api/menu-items/`
- **Body** (JSON):
  ```json
  {
      "name": "Test Pizza",
      "price": 0,
      "category": 1,
      "is_available": true
  }
  ```
- **Expected Status**: `400 Bad Request`

### 6. Test Quantity Validation Error
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/api/orders/`
- **Header**: `Authorization: Token <token>`
- **Body** (JSON):
  ```json
  {
      "item": "Pizza",
      "quantity": 0,
      "status": "pending"
  }
  ```
- **Expected Status**: `400 Bad Request`

### 7. GET Orders
- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/api/orders/`
- **Expected Status**: `200 OK`

### 8. Order Pagination
- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/api/orders/?page=1`
- **URL**: `http://127.0.0.1:8000/api/orders/?page=2`
- **Expected Status**: `200 OK`

### 9. Status Filtering
- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/api/orders/?status=pending`
- **Expected Status**: `200 OK`

### 10. Generate Auth Token
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/api-token-auth/`
- **Body** (JSON):
  ```json
  {
      "username": "testuser",
      "password": "testpassword"
  }
  ```
- **Expected Status**: `200 OK`

### 11. Authenticated Order Creation
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/api/orders/`
- **Header**: `Authorization: Token 487c2113cd61d046d733b1d5a3f45017aab432e1`
- **Body** (JSON):
  ```json
  {
      "item": "Cheese Burger",
      "quantity": 2,
      "status": "pending"
  }
  ```
- **Expected Status**: `201 Created` (`customer` automatically set to `"testuser"`).

### 12. My Orders History
- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/api/my-orders/`
- **Header**: `Authorization: Token 487c2113cd61d046d733b1d5a3f45017aab432e1`
- **Expected Status**: `200 OK`

### 13. Unauthenticated Access to My Orders
- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/api/my-orders/`
- *(Without Authorization header)*
- **Expected Status**: `401 Unauthorized`

---

## Postman Screenshots

> [!NOTE]
> Capture actual Postman screenshots when running the server locally and place the image files inside the `docs/screenshots/` directory.

Placeholders for submission screenshots:

1. **Category GET**: Save screenshot to `docs/screenshots/01_category_get.png`
2. **Category POST**: Save screenshot to `docs/screenshots/02_category_post.png`
3. **MenuItem POST**: Save screenshot to `docs/screenshots/03_menuitem_post.png`
4. **MenuItem Validation Error**: Save screenshot to `docs/screenshots/04_menuitem_validation_error.png`
5. **Order GET**: Save screenshot to `docs/screenshots/05_order_get.png`
6. **Order Pagination**: Save screenshot to `docs/screenshots/06_order_pagination.png`
7. **Order Status Filtering**: Save screenshot to `docs/screenshots/07_order_status_filtering.png`
8. **Token Generation**: Save screenshot to `docs/screenshots/08_token_generation.png`
9. **Authenticated Order Creation**: Save screenshot to `docs/screenshots/09_authenticated_order_creation.png`
10. **My Orders**: Save screenshot to `docs/screenshots/10_my_orders.png`
11. **Unauthenticated 401 Response**: Save screenshot to `docs/screenshots/11_unauthenticated_401.png`
