from django.urls import path
from .views import RestaurantViewAPI

urlpatterns = [
    path('restaurants/', RestaurantViewAPI.as_view()),
    # path('create-restaurant/', CreateRestaurantAPI.as_view()),
]
