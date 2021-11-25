from django.urls import path
from .views import RestaurantAPI, MenuCategoryAPI, MenuAPI

urlpatterns = [
    path('restaurants/', RestaurantAPI.as_view()),
    path('menucategories/', MenuCategoryAPI.as_view()),
    path('menus/', MenuAPI.as_view()),
]
