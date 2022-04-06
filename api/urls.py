from django.urls import path
from .views import RestaurantAPIView, RestaurantAPIDetailView, MenuCategoryAPIView, MenuCategoryDetailAPIView, \
    MenuAPIView, MenuDetailAPIView, MenuCategoryListBasedOnRestaurantAPIView, RestaurantCategoryAPIView, \
    RestaurantBasedOnTypesAPIView, CheckSimilarityOfRestaurants, GetSimilarRestaurants, \
    TableListBasedOnRestaurantAPIView, ConfirmTableBookingAPIView, ReservedTableListByUserAPIView, \
    GetSimilarityPercentageSerializer, FavouriteRestaurant, IsFavouriteAPI, EditFavourite, CalculateRecommendation, \
    GetTagsAPIView

from django.conf.urls.static import static
from crabackend import settings

urlpatterns = [
                  path('restaurants/', RestaurantAPIView.as_view()),
                  path('restaurant-types/', RestaurantCategoryAPIView.as_view()),
                  path('restaurant-type/<int:id>', RestaurantBasedOnTypesAPIView.as_view()),
                  path('restaurant/<int:id>', RestaurantAPIDetailView.as_view()),
                  path('menucategories/', MenuCategoryAPIView.as_view()),
                  path('menucategory/<int:id>', MenuCategoryDetailAPIView.as_view()),
                  path('menus/', MenuAPIView.as_view()),
                  path('menu/<int:id>', MenuDetailAPIView.as_view()),
                  path('tags/', GetTagsAPIView.as_view()),
                  path('restaurant/<int:id>/menuList', MenuCategoryListBasedOnRestaurantAPIView.as_view()),
                  path('restaurant/<int:id>/tableList', TableListBasedOnRestaurantAPIView.as_view()),
                  path('restaurant-booking/', ConfirmTableBookingAPIView.as_view()),
                  path('restaurant-recommendation/', CalculateRecommendation.as_view()),
                  path('restaurant-similarity/', CheckSimilarityOfRestaurants.as_view()),
                  path('restaurant-similarities/<int:id>', GetSimilarRestaurants.as_view()),
                  path('favourite-restaurants/<str:username>', FavouriteRestaurant.as_view()),
                  path('edit-fav/', EditFavourite.as_view()),
                  path('restaurant-similarities-percent/<int:id>', GetSimilarityPercentageSerializer.as_view()),
                  path('my-reservations/<int:id>', ReservedTableListByUserAPIView.as_view()),
                  path('is-favourite/', IsFavouriteAPI.as_view()),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
