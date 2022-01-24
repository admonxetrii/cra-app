from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import AuthAPIView, CustomUserCreate, LogoutView, UserDetailAPIView, VerifyOtp, ForgotPassword, \
    ChangePassword

urlpatterns = [
    path('me/', UserDetailAPIView.as_view()),
    path('register/', CustomUserCreate.as_view()),
    path('verify-otp/', VerifyOtp.as_view()),
    path('forgot-password/', ForgotPassword.as_view()),
    path('change-password/', ChangePassword.as_view()),
    path('token/', AuthAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
