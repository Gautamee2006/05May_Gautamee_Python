from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('',views.index),
    path('login/<int:id>',views.login,name='login'),
    path("showdata/", views.showdata, name="showdata"),
    path("updatedata/<int:id>/", views.updatedata, name="updatedata"),
    path("deletedata/<int:id>/", views.deletedata, name="deletedata"),
]
