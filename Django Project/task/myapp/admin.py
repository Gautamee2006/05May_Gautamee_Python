from django.contrib import admin
from .models import *

class user(admin.ModelAdmin):
    list_display=['id','name','age','email','mobile','address']

admin.site.register(userinfo,user)


