from django.urls import path
from admin_panel.views import (
    dashboard_view,
    restaurant_list, restaurant_add, restaurant_edit, restaurant_delete, restaurant_toggle,
    menu_list, category_add, category_delete, food_item_add, food_item_edit, food_item_delete, food_item_toggle,
    order_list, order_detail, order_update_status,
    reservation_list, reservation_update_status,
    customer_list, customer_detail, customer_toggle,
    review_list, review_toggle, review_delete,
    offer_list, offer_add, offer_edit, offer_delete, offer_toggle,
    location_list, location_add, location_delete, cuisine_list, cuisine_add, cuisine_delete,
    analytics_view,
)

urlpatterns = [
    # Dashboard
    path('', dashboard_view, name='panel_dashboard'),

    # Restaurants
    path('restaurants/', restaurant_list, name='panel_restaurant_list'),
    path('restaurants/add/', restaurant_add, name='panel_restaurant_add'),
    path('restaurants/<int:pk>/edit/', restaurant_edit, name='panel_restaurant_edit'),
    path('restaurants/<int:pk>/delete/', restaurant_delete, name='panel_restaurant_delete'),
    path('restaurants/<int:pk>/toggle/', restaurant_toggle, name='panel_restaurant_toggle'),

    # Menu
    path('menu/', menu_list, name='panel_menu_list'),
    path('menu/category/add/', category_add, name='panel_category_add'),
    path('menu/category/<int:pk>/delete/', category_delete, name='panel_category_delete'),
    path('menu/item/add/', food_item_add, name='panel_food_item_add'),
    path('menu/item/<int:pk>/edit/', food_item_edit, name='panel_food_item_edit'),
    path('menu/item/<int:pk>/delete/', food_item_delete, name='panel_food_item_delete'),
    path('menu/item/<int:pk>/toggle/', food_item_toggle, name='panel_food_item_toggle'),

    # Orders
    path('orders/', order_list, name='panel_order_list'),
    path('orders/<int:pk>/', order_detail, name='panel_order_detail'),
    path('orders/<int:pk>/status/', order_update_status, name='panel_order_update_status'),

    # Reservations
    path('reservations/', reservation_list, name='panel_reservation_list'),
    path('reservations/<int:pk>/status/', reservation_update_status, name='panel_reservation_update_status'),

    # Customers
    path('customers/', customer_list, name='panel_customer_list'),
    path('customers/<int:pk>/', customer_detail, name='panel_customer_detail'),
    path('customers/<int:pk>/toggle/', customer_toggle, name='panel_customer_toggle'),

    # Reviews
    path('reviews/', review_list, name='panel_review_list'),
    path('reviews/<int:pk>/toggle/', review_toggle, name='panel_review_toggle'),
    path('reviews/<int:pk>/delete/', review_delete, name='panel_review_delete'),

    # Offers
    path('offers/', offer_list, name='panel_offer_list'),
    path('offers/add/', offer_add, name='panel_offer_add'),
    path('offers/<int:pk>/edit/', offer_edit, name='panel_offer_edit'),
    path('offers/<int:pk>/delete/', offer_delete, name='panel_offer_delete'),
    path('offers/<int:pk>/toggle/', offer_toggle, name='panel_offer_toggle'),

    # Locations & Cuisines
    path('locations/', location_list, name='panel_location_list'),
    path('locations/add/', location_add, name='panel_location_add'),
    path('locations/<int:pk>/delete/', location_delete, name='panel_location_delete'),
    path('locations/cuisines/', cuisine_list, name='panel_cuisine_list'),
    path('locations/cuisines/add/', cuisine_add, name='panel_cuisine_add'),
    path('locations/cuisines/<int:pk>/delete/', cuisine_delete, name='panel_cuisine_delete'),

    # Analytics
    path('analytics/', analytics_view, name='panel_analytics'),
]
