from django import views
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from JWTApp.views import CreateAndListDataView, ProductDetailsView, UserLoginView, UserLogoutView, UserRegisterView


urlpatterns = [
    # jwt
    path("jwt/create/", TokenObtainPairView.as_view(), name="create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="verify"),


    # user details
    path("userdetail/", CreateAndListDataView.as_view(), name="createuser"),

    # user register
    path("userregister/", UserRegisterView.as_view(), name="user-register"),
    path("userlogin/", UserLoginView.as_view(), name="user-login"),
    path("userlogout/", UserLogoutView.as_view(), name="user-logout"),



    #product
    path("product/",ProductDetailsView.as_view(),name="produc")
]
