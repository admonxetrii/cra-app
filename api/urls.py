from django.urls import path
from .views import RestaurantViewAPI, CreateRestaurantAPI, DetailRestaurantAPI, UpdateRestaurantAPI, DeleteRestaurantAPI

urlpatterns = [
    path('restaurants/', RestaurantViewAPI.as_view()),
    path('create-restaurant/', CreateRestaurantAPI.as_view()),
    path('get-restaurant/<int:id>', DetailRestaurantAPI.as_view()),
    path('update-restaurant/<int:id>', UpdateRestaurantAPI.as_view()),
    path('delete-restaurant/<int:id>', DeleteRestaurantAPI.as_view()),
]
