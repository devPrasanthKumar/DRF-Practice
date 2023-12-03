from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class ProductDetailsModel(models.Model):
    product_name = models.CharField(max_length=300)
    product_slug = models.SlugField(unique=True, max_length=300)
    product_created_at = models.DateTimeField(auto_now_add=False)
    product_updated_at = models.DateTimeField(auto_now=False)
    user_name = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="product")

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        if not self.product_slug:
            self.product_slug = slugify(self.product_name)
        super(ProductDetailsModel, self).save(*args, **kwargs)
