from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import AuthAPIView, RegisterAPIView, LogoutView

urlpatterns = [
    # path('', AuthAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('token/', AuthAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
