from django.urls import path
from .views import RestaurantViewAPI

# , RestaurantCreateAPI, RestaurantDetailAPI, RestaurantUpdateAPI, RestaurantDeleteAPI

urlpatterns = [
    path('restaurants/', RestaurantViewAPI.as_view()),
    # path('create-restaurant/', RestaurantCreateAPI.as_view()),
    # path('get-restaurant/<int:id>', RestaurantDetailAPI.as_view()),
    # path('update-restaurant/<int:id>', RestaurantUpdateAPI.as_view()),
    # path('delete-restaurant/<int:id>', RestaurantDeleteAPI.as_view()),
]
