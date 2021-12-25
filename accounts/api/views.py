import jwt
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.models import CustomUser

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
    permission_classes = [permissions.AllowAny]
    serializer_class = UserProfileSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'username'


class CustomUserCreate(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        print(request.data)
        reg_serializer = UserRegisterSerializer(data=request.data)
        if reg_serializer.is_valid():
            newuser = reg_serializer.save()
            if newuser:
                return Response(status=status.HTTP_201_CREATED)
            return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

