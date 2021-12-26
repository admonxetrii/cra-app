from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import AuthAPIView, CustomUserCreate, LogoutView, UserDetailAPIView

urlpatterns = [
    path('me/', UserDetailAPIView.as_view()),
    path('register/', CustomUserCreate.as_view()),
    path('token/', AuthAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
