from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type', 'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type', 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
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
        return user_obj
