from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list_view, name='list'),
    path('mark-read/<int:notification_id>/', views.mark_notification_read_view, name='mark_read'),
]
