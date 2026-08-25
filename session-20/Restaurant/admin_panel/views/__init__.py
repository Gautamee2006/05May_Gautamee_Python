from .dashboard import dashboard_view
from .restaurants import (
    restaurant_list, restaurant_add, restaurant_edit, restaurant_delete, restaurant_toggle
)
from .menu import (
    menu_list, category_add, category_delete,
    food_item_add, food_item_edit, food_item_delete, food_item_toggle
)
from .orders import order_list, order_detail, order_update_status
from .reservations import reservation_list, reservation_update_status
from .customers import customer_list, customer_detail, customer_toggle
from .reviews import review_list, review_toggle, review_delete
from .offers import offer_list, offer_add, offer_edit, offer_delete, offer_toggle
from .locations import location_list, location_add, location_delete, cuisine_list, cuisine_add, cuisine_delete
from .analytics import analytics_view
