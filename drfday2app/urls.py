from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path("createaccount/", views.UserAccountView.as_view(), name="create"),
    path("login/", obtain_auth_token, name="login"),
    path("logout/", views.UserAccountLogoutView.as_view(), name="logout"),
    path("user-login/", views.UserAccountLoginView.as_view(), name="user-login"),

    # product
    path("showproduct/", views.ProductDetailsView.as_view(), name="showproduct"),
]
