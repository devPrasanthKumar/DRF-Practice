from rest_framework import serializers
from .models import AddDetailsModel, UserProductDetails

from django.contrib.auth.models import User


class AddDetailsSerializer(serializers.Serializer):
    user_name = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    content = serializers.CharField()
    date = serializers.DateTimeField(read_only=True)
    is_finished = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return AddDetailsModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user_name.username = validated_data.get(
            "user_name", instance.user_name.username)
        instance.content = validated_data.get("content", instance.content)
        instance.date = validated_data.get("data", instance.date)
        instance.is_finished = validated_data.get(
            "is_finished", instance.is_finished)
        instance.save()
        return instance


class AddDetailsSimpleSerializer(serializers.ModelSerializer):
    detailss = AddDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = UserProductDetails
        fields = "__all__"
