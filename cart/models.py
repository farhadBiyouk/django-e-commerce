from django.db import models
from django.contrib.auth.models import User
from home.models import Product, Variant


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.product.name


class Compare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.product.name
