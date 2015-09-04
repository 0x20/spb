from django.db import models
from SmarterSpaceBrain.models import SpaceUser

# Create your models here

class Badges(models.Model):
    user = models.ForeignKey(SpaceUser)
    number = models.CharField(max_length=12)
    own = models.BooleanField()

class GatekeeperSchedules(models.Model):

    DAYS = (
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday'),
    )

    day = models.IntegerField(choices=DAYS)
    starttime = models.TimeField()
    endtime = models.TimeField()

class Phonenumbers:

    user = models.ForeignKey(SpaceUser)
    phonenumber = models.TextField()
    cellphone = models.BooleanField()
