from django.contrib import admin
from .models import Restaurant, MenuCategory, Menu, RestaurantType, RestaurantFeaturedMenu, \
    RestaurantFeaturedMenuForRestaurant, RestaurantTable, RestaurantFloorLevel, LikeTags

# Register your models here.
admin.site.register(LikeTags)
admin.site.register(Restaurant)
admin.site.register(MenuCategory)
admin.site.register(Menu)
admin.site.register(RestaurantType)
admin.site.register(RestaurantFeaturedMenu)
admin.site.register(RestaurantFeaturedMenuForRestaurant)
admin.site.register(RestaurantTable)
admin.site.register(RestaurantFloorLevel)
