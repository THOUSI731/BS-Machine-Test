from rest_framework import serializers
from ..models import Account, UserProfile
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserAccountSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = Account
        fields = "__all__"

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise ValidationError("Password is not Correct")
        return attrs


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email

        return token

class UserProfileSerialier(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
     profile=UserProfileSerialier()
     class Meta:
          model=Account
          fields="__all__"          

