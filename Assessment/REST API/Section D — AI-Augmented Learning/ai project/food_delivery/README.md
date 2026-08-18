# Food Delivery - Order Placement API

A beginner-friendly Django REST Framework (DRF) project implementing a POST endpoint for placing customer food orders using DRF `APIView`, `ModelSerializer`, and SQLite.

---

## 1. Objective

The objective of this project is to build a robust, simple REST API that accepts customer order details (`customer_name`, `item`, `quantity`), validates the input (ensuring `quantity` is a positive integer), saves valid orders to the SQLite database, and returns the created order details along with an auto-generated primary key ID.

---

## 2. Technologies Used

- **Python**: 3.x
- **Django**: Web Framework
- **Django REST Framework (DRF)**: RESTful API development (`APIView`, `ModelSerializer`)
- **SQLite**: Default relational database
- **Postman**: API testing and verification

---

## 3. Project Structure

```text
food_delivery/
│
├── manage.py
│
├── food_delivery/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── orders/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
│       └── 0001_initial.py
│
├── docs/
│   └── screenshots/
│       └── .gitkeep
│
└── README.md
```

---

## 4. Installation Steps

1. **Clone or navigate to the project repository**:
   ```bash
   cd food_delivery
   ```

2. **Ensure Django and Django REST Framework are installed**:
   ```bash
   pip install django djangorestframework
   ```

---

## 5. Migration Commands

To prepare the SQLite database and create the `orders_order` table, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

Optionally, create a superuser to access the Django Admin panel:

```bash
python manage.py createsuperuser
```

---

## 6. Run Server Command

Start the local Django development server:

```bash
python manage.py runserver
```

The server will start running at: `http://127.0.0.1:8000/`

---

## 7. API Endpoint

- **Endpoint**: `/api/orders/place/`
- **Full URL**: `http://127.0.0.1:8000/api/orders/place/`
- **HTTP Method**: `POST`
- **Content-Type**: `application/json`

---

## 8. Request Format

Send a JSON payload containing `customer_name`, `item`, and `quantity` in the request body.

```json
{
    "customer_name": "Gautamee",
    "item": "Pizza",
    "quantity": 2
}
```

---

## 9. Successful Response

If the input is valid (`quantity` > 0), the API saves the order to SQLite and returns the saved order details with HTTP status `201 Created`.

**HTTP Status**: `201 Created`

**Response Body**:
```json
{
    "id": 1,
    "customer_name": "Gautamee",
    "item": "Pizza",
    "quantity": 2
}
```

---

## 10. Validation Failure Response

If `quantity` is 0, negative, or invalid:
- The order is **NOT** saved to the database.
- The API returns HTTP status `400 Bad Request`.

### Example 1: `quantity` is 0 or negative (`quantity: 0` or `quantity: -1`)

**HTTP Status**: `400 Bad Request`

**Response Body**:
```json
{
    "quantity": [
        "Quantity must be a positive integer."
    ]
}
```

### Example 2: Invalid/non-integer value (`quantity: "abc"`)

**HTTP Status**: `400 Bad Request`

**Response Body**:
```json
{
    "quantity": [
        "A valid integer is required."
    ]
}
```

---

## 11. Postman Testing

Follow these steps to test the API end-to-end using Postman:

### Test 1: Successful Order Creation

1. Open Postman and select HTTP method **POST**.
2. Enter URL: `http://127.0.0.1:8000/api/orders/place/`
3. In the **Headers** tab, add:
   - Key: `Content-Type`
   - Value: `application/json`
4. In the **Body** tab, select **raw** and set type to **JSON**.
5. Paste the payload:
   ```json
   {
       "customer_name": "Gautamee",
       "item": "Pizza",
       "quantity": 2
   }
   ```
6. Click **Send**.
7. Verify that the response returns **HTTP Status 201 Created** with the auto-generated `id`.

---

### Test 2: Validation Failure (Invalid Quantity)

1. Set HTTP method to **POST**.
2. Enter URL: `http://127.0.0.1:8000/api/orders/place/`
3. In the **Body** tab (raw JSON), paste:
   ```json
   {
       "customer_name": "Gautamee",
       "item": "Pizza",
       "quantity": 0
   }
   ```
4. Click **Send**.
5. Verify that the response returns **HTTP Status 400 Bad Request** with message:
   `{"quantity": ["Quantity must be a positive integer."]}`
6. Repeat the test with `quantity: -1` and `quantity: "abc"`.

---

## 12. Screenshot Instructions

Please capture screenshots from the actual Postman application during testing:

1. **Successful POST Request Screenshot**:
   - Must show the URL (`http://127.0.0.1:8000/api/orders/place/`), Request JSON body (`quantity: 2`), **HTTP 201 Created** status, and the response body with auto-generated `id`.
   - Save image as: `docs/screenshots/1_success_postman.png`

2. **Validation Failure POST Request Screenshot**:
   - Must show the URL, Request JSON body (`quantity: 0` or `-1`), **HTTP 400 Bad Request** status, and the validation error message (`"Quantity must be a positive integer."`).
   - Save image as: `docs/screenshots/2_validation_failure_postman.png`

All screenshots can be placed in the `docs/screenshots/` directory for documentation submission.

---

## 13. Django Admin Verification

1. Start server: `python manage.py runserver`
2. Open browser at: `http://127.0.0.1:8000/admin/`
3. Log in using superuser credentials (`admin` / `admin123`).
4. Click on **Orders** under the **ORDERS** app.
5. Verify created orders are listed with ID, customer name, item, and quantity.
