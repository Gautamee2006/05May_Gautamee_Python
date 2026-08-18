# Postman Screenshots Directory

This directory is reserved for capturing and storing sample Postman screenshots for the API submission.

Required screenshots to place in this folder:

1. `01_category_get.png` - Category GET request (`GET http://127.0.0.1:8000/api/categories/`)
2. `02_category_post.png` - Category POST request (`POST http://127.0.0.1:8000/api/categories/`)
3. `03_menuitem_post.png` - MenuItem POST request (`POST http://127.0.0.1:8000/api/menu-items/`)
4. `04_menuitem_validation_error.png` - MenuItem validation error (`price <= 0` returning 400)
5. `05_order_get.png` - Order GET request (`GET http://127.0.0.1:8000/api/orders/`)
6. `06_order_pagination.png` - Order pagination request (`GET http://127.0.0.1:8000/api/orders/?page=2`)
7. `07_order_status_filtering.png` - Order status filtering request (`GET http://127.0.0.1:8000/api/orders/?status=pending`)
8. `08_token_generation.png` - Token generation request (`POST http://127.0.0.1:8000/api-token-auth/`)
9. `09_authenticated_order_creation.png` - Authenticated order creation (`POST http://127.0.0.1:8000/api/orders/` with `Authorization: Token <token>`)
10. `10_my_orders.png` - User order history (`GET http://127.0.0.1:8000/api/my-orders/` with Token)
11. `11_unauthenticated_401.png` - Unauthenticated request (`GET http://127.0.0.1:8000/api/my-orders/` returning 401 Unauthorized)
