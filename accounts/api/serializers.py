import datetime
from django.utils import timezone
from rest_framework import serializers
from accounts.models import CustomUser

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'street',
            'city',
            'state',
            'about',
            'profile_picture',
            'is_active',
            'is_superuser',
            'is_staff',
            'is_customer',
            'is_premium_customer',
            'is_waiter',
            'date_joined'
        ]


class UserLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type', 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'password',
            'confirm_password',
            'phone_number',
            'first_name',
            'last_name',
            'street',
            'city',
            'state',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        qs = CustomUser.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        qs = CustomUser.objects.filter(username__iexact=value)
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
        password = validated_data.pop('password', None)
        user_obj = self.Meta.model(**validated_data)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj
