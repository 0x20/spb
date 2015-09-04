from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class SpaceUser(AbstractUser):

    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    TYPES = (
        ('F', 'Full member'),
        ('R', 'Reduction member'),
    )

    membertype = models.CharField(max_length=1, choices=TYPES)
    paymentstring = models.CharField(max_length=18)


