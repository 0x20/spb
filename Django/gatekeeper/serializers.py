from rest_framework import serializers
from gatekeeper.models import Badges

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badges

