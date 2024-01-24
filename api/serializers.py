from rest_framework import serializers
from .models import weatherData, weatherStats

# serializer for the weather data
class dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = weatherData
        fields = ('station', 'date', 'max_temp','min_temp','precip')

# serializaer for the weather stats
class statSerializer(serializers.ModelSerializer):
    class Meta:
        model = weatherStats
        fields = ('station', 'year','max_temp_mean','min_temp_mean','total_precip')