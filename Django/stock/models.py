from django.db import models
from SmarterSpaceBrain.models import SpaceUser

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    cost = models.IntegerField()

class ProductHistoryType(models.Model):
    type = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class ProductHistory(models.Model):
    product = models.ForeignKey(Product)
    type = models.ForeignKey(ProductHistoryType)
    changeamount = models.IntegerField()
    user = models.ForeignKey(SpaceUser)
