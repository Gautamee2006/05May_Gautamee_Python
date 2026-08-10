from django.contrib import admin

from .models import InfluencerProfile


@admin.register(InfluencerProfile)
class InfluencerProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'display_name',
        'phone_number',
    )