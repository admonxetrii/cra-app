from django.urls import path
from .views import RestaurantAPIView, RestaurantAPIDetailView, MenuCategoryAPIView, MenuCategoryDetailAPIView, \
    MenuAPIView, MenuDetailAPIView, MenuCategoryListBasedOnRestaurantAPIView

from django.conf.urls.static import static
from crabackend import settings

urlpatterns = [
                  path('restaurants/', RestaurantAPIView.as_view()),
                  path('restaurant/<int:id>', RestaurantAPIDetailView.as_view()),
                  path('menucategories/', MenuCategoryAPIView.as_view()),
                  path('menucategory/<int:id>', MenuCategoryDetailAPIView.as_view()),
                  path('menus/', MenuAPIView.as_view()),
                  path('menu/<int:id>', MenuDetailAPIView.as_view()),
                  path('restaurant/<int:id>/menuList', MenuCategoryListBasedOnRestaurantAPIView.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
