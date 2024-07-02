from core.models import Venue
from rest_framework import serializers


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'
