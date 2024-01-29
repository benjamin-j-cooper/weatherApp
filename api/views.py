from django.shortcuts import render

from .models import weatherData, weatherStats
from .serializers import dataSerializer, statSerializer
from .filters import dataFilter, statsFilter

from rest_framework import generics, mixins

class weather_Data_View(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = weatherData.objects.all()
    serializer_class = dataSerializer
    filterset_class = dataFilter

    def get(self, request, *args, **kwargs):
        return self.list(request)

weather_view = weather_Data_View.as_view()

class weather_Stats_View(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = weatherStats.objects.all()
    serializer_class = statSerializer
    filterset_class = statsFilter

    def get(self, request, *args, **kwargs):
        return self.list(request)

stats_view = weather_Stats_View.as_view()
