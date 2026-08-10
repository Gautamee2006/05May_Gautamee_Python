from django.contrib import admin

from .models import (
    Restaurant,
    Movie,
    Review,
    Category,
    Product
)


admin.site.register(Restaurant)

admin.site.register(Movie)

admin.site.register(Review)

admin.site.register(Category)

admin.site.register(Product)