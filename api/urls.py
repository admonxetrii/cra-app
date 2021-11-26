from django.urls import path
from .views import RestaurantAPIView, RestaurantAPIDetailView, MenuCategoryAPI, MenuAPI

urlpatterns = [
    path('restaurants/', RestaurantAPIView.as_view()),
    path('restaurant/<int:id>', RestaurantAPIDetailView.as_view()),
    path('menucategories/', MenuCategoryAPI.as_view()),
    path('menus/', MenuAPI.as_view()),
]
