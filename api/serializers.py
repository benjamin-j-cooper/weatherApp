from rest_framework import serializers
from .models import weatherData, weatherStats

# serializer for the weather data
class dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = weatherData
        fields = '__all__'

# serializaer for the weather stats
class statSerializer(serializers.ModelSerializer):
    class Meta:
        model = weatherStats
        fields = '__all__'