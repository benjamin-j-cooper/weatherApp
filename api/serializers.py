from rest_framework import serializers
from .models import weatherData, weatherStats

class dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = weatherData
        fields = ('station', 'date', 'max_temp','min_temp','precip')

class statsSerializer(serializers.ModelSerializer):
    class Meta:
        model = weatherStats
        fields = ('station', 'year','max_temp_mean','min_temp_mean','total_precip')