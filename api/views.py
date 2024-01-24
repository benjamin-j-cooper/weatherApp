from django.shortcuts import render

from .models import weatherData, weatherStats
from .serializers import dataSerializer, statSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics

@api_view(['GET'])
def api_home(request, *args, **kwargs):
    return 

@api_view(['GET'])
def weather(request, *args, **kwargs):
    instance = weatherData.objects.all().order_by().first()
    data = {}
    if instance:
        data = dataSerializer(instance).data
    return Response(data)

@api_view(['GET'])
def stats(request, *args, **kwargs):
    instance = weatherStats.objects.all().order_by().first()
    data = {}
    if instance:
        data = statSerializer(instance).data
    return Response(data)

# class dataCreateAPIView(generics.CreateAPIView):
#     queryset = weatherData.objects.all()
#     serializer_class = dataSerializer

# class dataDetailAPIView(generics.RetrieveAPIView):
#     queryset = weatherData.objects.all()
#     serializer_class = dataSerializer
#     lookup_field = 'station'
    