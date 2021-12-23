import datetime
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model

from accounts.models import UserProfile

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_admin', 'is_staff')


class UserProfileSerializer(serializers.ModelSerializer):
    userprofile = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('userprofile', 'state', 'city', 'phonenumber')
        read_only_fields = ['user']


class UserDetailSerializer(serializers.Serializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'uri',
        ]

    def get_uri(self, obj):
        return "/api/user/{id}/".format(id=obj.username)

    def get_status_list(self, obj):
        return "obj"


class UserPublicSerializer(serializers.Serializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'uri',
        ]

    def get_uri(self, obj):
        return "/api/users/{id}/".format(id=obj.id)


class UserLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token


class UserRegisterSerializer(serializers.Serializer):
    confirm_password = serializers.CharField(style={'input_type', 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone_number'
            'password',
            'confirm_password',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate(self, data):
        pw = data.get('password')
        cpw = data.get('confirm_password')
        if pw != cpw:
            raise serializers.ValidationError("Password must match")
        return data

    def create(self, validated_data):
        print(validated_data)
        user_obj = User(username=validated_data.get('username'), email=validated_data.get('email'))
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        created_user = User.objects.get(username=validated_data.username)
        user_profile = User.objects.create(user_id=created_user.id)
        user_profile.save()
        return user_obj
