
from rest_framework import serializers
from .models import *
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as knoxLoginView
from django.contrib.auth import get_user_model


class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            # username=validated_data['username'],
            email=validated_data['email'],
            # password=validated_data['password']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LogoutAllSerializer(serializers.Serializer):
    pass


# class ChangePasswordSerializer(serializers.Serializer):
#     current_password = serializers.CharField()
#     new_password = serializers.CharField()


# LOGIN   
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


# All Users 
class AllUsersSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

# class AllUsersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['email', 'password']

# class LogoutView(serializers.Serializer):
class ActiveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        # fields = ['id', 'email', 'first_name', 'last_name']
        fields ='__all__'
# 


# class ResetPasswordLinkSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ResetPassword
#         fields = ('user_id', 'key', 'time')




class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class ResetPasswordLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResetPassword
        fields = ('user_id', 'key', 'time')


class ResetPasswordsSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    key = serializers.CharField(max_length=25)

