from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('restaurants.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('favorites.urls')),
    path('', include('reviews.urls')),
    path('', include('reservations.urls')),
    path('', include('offers.urls')),
    path('', include('cart.urls')),
    path('', include('orders.urls')),
    path('panel/', include('admin_panel.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
