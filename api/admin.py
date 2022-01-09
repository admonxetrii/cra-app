from django.contrib import admin
from .models import Restaurant, MenuCategory, Menu, RestaurantType, RestaurantFeaturedMenu, \
    RestaurantFeaturedMenuForRestaurant

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(MenuCategory)
admin.site.register(Menu)
admin.site.register(RestaurantType)
admin.site.register(RestaurantFeaturedMenu)
admin.site.register(RestaurantFeaturedMenuForRestaurant)
