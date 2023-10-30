from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Account, UserProfile
from rest_framework_simplejwt.views import TokenObtainPairView
from .api.serializers import (
    MyTokenObtainPairSerializer,
    UserAccountSerializer,
    UserSerializer,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Account
from django.shortcuts import get_object_or_404


class UserRegisterationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserAccountSerializer(data=request.data)
        if serializer.is_valid():
            user = Account.objects.create(
                first_name=serializer.validated_data.get("first_name", None),
                last_name=serializer.validated_data.get("last_name", None),
                email=serializer.validated_data.get("email", None),
                username=serializer.validated_data.get("username", None),
            )
            user.set_password(serializer.validated_data["password"])
            user.save(update_fields=["password"])
            UserProfile.objects.create(user=user)
            
            return Response(
                {"msg": "Registeration Successful", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairAPIView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserProfileDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = UserProfile.objects.filter(user_id=request.user.id)
        serializer=UserSerializer(data=request.data,user=request.user)
        if serializer.is_valid():
             instance.profile_picture=serializer.validated_data.get("profile_picture",instance.profile_picture)
             instance.date_of_birth = serializer.validated_data.get("date_of_birth",instance.date_of_birth)
             instance.save()
             return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  
        
