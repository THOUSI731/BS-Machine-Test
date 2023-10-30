from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Account, UserProfile
from rest_framework_simplejwt.views import TokenObtainPairView
from .api.serializers import (
    MyTokenObtainPairSerializer,
    UserAccountSerializer,
    UserProfileSerialier,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Account

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
        user=Account.objects.filter(email=request.user).select_related('profile')
        return Response(UserProfileSerialier(user).data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = UserProfile.objects.filter(user_id=request.user.id)
        print(instance)
        
