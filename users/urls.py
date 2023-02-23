from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserLoginView, UserRegistrationView

app_name = "user"

urlpatterns = [
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
