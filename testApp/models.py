from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.utils import timezone


class AddDetailsModel(models.Model):
    user_name = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="details")
    content = models.CharField(max_length=300)
    date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return str(self.content)


class UserProductDetails(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_price = models.FloatField()
    details_model = models.ForeignKey(
        AddDetailsModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name
