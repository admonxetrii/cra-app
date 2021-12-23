import jwt
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import AnonPermissionOnly
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from .serializers import UserRegisterSerializer, UserDetailSerializer, UserProfileSerializer, UserLoginSerializer
from ..models import UserProfile

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
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'username'


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AnonPermissionOnly]


class UserProfileViewSet(generics.GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get(self, request):
        userProfileObj = User.objects.filter(id=request.user.id)
        serializer = self.get_serializer(userProfileObj)
        return Response(serializer.data)

# class RegisterAPIView(APIView):
#     serializer_class = UserRegisterSerializer
#     def post(self, request, *args, **kwargs):
#         permission_classes = [permissions.AllowAny]
#         print(request.user)
#         if request.user.is_authenticated():
#             return Response({'detail': 'You are already authenticated'}, status=400)
#         username = request.get('username')
#         email = request.get('email')
#         password = request.get('password')
#         confirm_password = request.get('confpass')
#         qs = User.objects.filter(
#             Q(username__iexact=username) |
#             Q(email__iexact=email)
#         ).distinct()
#         if password != confirm_password:
#             return Response({"password": "Password doesn't match."}, status=401)
#         if qs.exists():
#             return Response({"details": "This user already exists."}, status=401)
#         else:
#             user = User.objects.create(username=username, email=email)
#             user.set_password(password)
#             user.save()
#             payload = jwt_payload_handler(user)
#             token = jwt_encode_handler(payload)
#             response = jwt_response_payload_handler(token, user, request=request)
#             return Response({"details": "Thank you for registering, please verify your email."}, status=201)
