from django.urls import path
from .. import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("", views.UserRegisterationAPIView.as_view(), name="user-register"),
    path("login/", views.MyTokenObtainPairAPIView.as_view(), name="user-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", views.UserProfileDetailAPIView.as_view(), name="token_refresh"),
]
