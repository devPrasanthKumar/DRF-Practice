from django.urls import path
from rest_framework.routers import DefaultRouter
# default  = DefaultRouter()
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("add/", views.add_details_view, name="add"),
    path("edit/<int:pk>", views.edit_details),
    path("search", views.search_detail),
    path("login/", obtain_auth_token, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # throtling  OTP Generator
    path('th/', views.view, name='th'),




]
