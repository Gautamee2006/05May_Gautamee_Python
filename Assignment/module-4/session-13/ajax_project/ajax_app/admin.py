from django.contrib import admin

from .models import (
    Song,
    Product,
    Movie,
    Playlist
)


admin.site.register(Song)

admin.site.register(Product)

admin.site.register(Movie)

admin.site.register(Playlist)