from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ProductDetailsModel(models.Model):
    username = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="product")
    product_name = models.CharField(max_length=300)
    product_description = models.TextField()
    product_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=False)
