from django.contrib import admin
from .models import Restaurant, MenuCategory, Menu

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(MenuCategory)
admin.site.register(Menu)
