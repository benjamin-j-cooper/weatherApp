from django.shortcuts import render

from .models import weatherData, weatherStats
from .serializers import dataSerializer, statSerializer
from .filters import dataFilter, statFilter

from rest_framework import generics, mixins

class weatherView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = weatherData.objects.all()
    serializer_class = dataSerializer
    filterset_class = dataFilter

    def get(self, request, *args, **kwargs):
        return self.list(request)

weather_view = weatherView.as_view()

class statsView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = weatherStats.objects.all()
    serializer_class = statSerializer
    filterset_class = statFilter

    def get(self, request, *args, **kwargs):
        return self.list(request)

stats_view = statsView.as_view()
