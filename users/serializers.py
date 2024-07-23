from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import User
from django.contrib.auth.models import Permission

class UserSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = User
        fields = ['id', 'username','password', 'email', 'first_name', 'last_name', 'is_active','password']#,'image','token'


    def validate(self, attrs):
     email = attrs.get("email")  # Use get() method to safely retrieve email field

     if email:
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise ValidationError("Email has already been used")

     return super().validate(attrs)


    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)

        user.set_password(password)

        user.save()


        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)




class PasswordResetSerializer(serializers.Serializer):

    new_password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    token = serializers.CharField()


class NewPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

