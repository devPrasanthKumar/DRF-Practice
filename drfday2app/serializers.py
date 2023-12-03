from .models import ProductDetailsModel
from rest_framework.serializers import ModelSerializer

# import built-in User model
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


""" create a serialzier for User account """


class UserAccountSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


"""  create a serialzer for product  """


class ProductDetailsSerializer(ModelSerializer):
    user_name = serializers.PrimaryKeyRelatedField(read_only=True)
    product_slug = serializers.SlugField(required=False)

    class Meta:
        model = ProductDetailsModel
        fields = "__all__"

    def create(self, validated_data):
        validated_data["user_name"] = self.context['request'].user
        print("my current user ", validated_data["user_name"])
        return super().create(validated_data)
