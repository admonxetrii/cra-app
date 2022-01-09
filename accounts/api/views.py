from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.models import CustomUser
from accounts.helpers import send_otp_to_email

from django.core.mail import send_mail
from crabackend import settings

from .permissions import AnonPermissionOnly
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserProfileSerializer

User = get_user_model()


class AuthAPIView(TokenObtainPairView):
    permission_classes = [AnonPermissionOnly]
    serializer_class = UserLoginSerializer


class LogoutView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = (permissions.IsAuthenticated)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class CustomUserCreate(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            print(request.data)
            reg_serializer = UserRegisterSerializer(data=request.data)

            if not reg_serializer.is_valid():
                return Response({"error": reg_serializer.errors, "status": status.HTTP_400_BAD_REQUEST})

            newuser = reg_serializer.save()
            if newuser:
                # send_email_token(newuser)
                return Response({"status": status.HTTP_201_CREATED,
                                 "message": "Successfully Registered.", "username": newuser.username})
            return Response({"message": "Cannot create user!!", "status": status.HTTP_400_BAD_REQUEST})
        except Exception as e:
            print(e)
            return Response({"message": "something went wrong", "status": status.HTTP_400_BAD_REQUEST})


class VerifyOtp(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            otpData = request.data
            print(request.data)
            user_obj = CustomUser.objects.get(username=otpData.get('username'))
            otp = otpData.get('otp')
            if user_obj.otp == otp:
                user_obj.is_verified = True
                user_obj.save()
                tokenr = RefreshToken.for_user(user_obj)
                return Response(
                    {"message": "Account verified!!", "status": status.HTTP_200_OK, "access": str(tokenr.access_token)})
            return Response({"message": "Invalid OTP", "status": status.HTTP_403_FORBIDDEN})

        except Exception as e:
            print(e)
        return Response({"message": "Something went wrong", "status": status.HTTP_400_BAD_REQUEST})

    def patch(self, request):
        try:
            data = request.data
            user_obj = CustomUser.objects.get(username=data.get('username'))

            if not user_obj.exists():
                return Response({"message": "No user found", "status": status.HTTP_404_NOT_FOUND})

            otpStatus, time = send_otp_to_email(data.get('email'), user_obj)
            if otpStatus:
                return Response({"message": "OTP sent successfully.", "status": status.HTTP_200_OK})
            return Response({"message": f"Try after {time} seconds", "status": status.HTTP_404_NOT_FOUND})

        except Exception as e:
            print(e)
        return Response({"message": "something went wrong", "status": status.HTTP_400_BAD_REQUEST})


def send_email_token(user_obj):
    try:
        subject = "Please verify your account for Pycemon Order"
        message = f"Hi, Your OTP verification code is {user_obj.otp} please verify your account."
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user_obj.email]
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        print(e)
    return "Cannot send OTP"
