from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import ProductDetailsModel


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "password"]


    def create(self,validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data) 


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetailsModel
        fields = "__all__"
