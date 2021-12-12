from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_jwt.settings import api_settings

from .serializers import UserRegisterSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()


class AuthAPIView(APIView):
    def post(self, request, *args, **kwargs):
        permission_classes = [permissions.AllowAny]
        print(request.user)
        if request.user.is_authenticated():
            return Response({'detail': 'You are already authenticated'}, status=400)
        username = request.get('username')
        password = request.get('password')
        qs = User.objects.filter(
            Q(username__iexact=username) |
            Q(email__iexact=username)
        ).distinct()
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, request=request)
                return Response(response)
        return Response({'details': 'Invalid Credentials'}, status=401)


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

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
