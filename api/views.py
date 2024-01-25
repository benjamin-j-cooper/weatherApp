from django.shortcuts import render

from .models import weatherData, weatherStats
from .serializers import dataSerializer, statSerializer
from .filters import dataFilter, statFilter

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, mixins
from django_filters import rest_framework as filters

# def api(request):
#     return render(request, 'home.html', {})

@api_view(['GET'])
def weather(request, *args, **kwargs):
    wxdata = weatherData.objects.all()[:20]
    data = {}
    if wxdata:
        data = dataSerializer(wxdata, many = True).data
    return Response(data)

@api_view(['GET'])
def stats(request, *args, **kwargs):
    wxstats = weatherStats.objects.all()[:20]
    stats = {}
    if wxstats:
        stats = statSerializer(wxstats, many = True).data
    return Response(stats)

class dataListAPIView(generics.ListCreateAPIView):
    queryset = weatherData.objects.all()
    serializer_class = dataSerializer
    filterset_class = dataFilter
    # filterset_fields = ('station','year')

data_list_view = dataListAPIView.as_view()

class statsListAPIView(generics.ListCreateAPIView):
    queryset = weatherStats.objects.all()
    serializer_class = statSerializer
    filterset_class = statFilter
    # filterset_fields = ('station','year')

stats_list_view = statsListAPIView.as_view()


class dataMixinView(mixins.ListModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = weatherData.objects.all()
    serializer_class = dataSerializer
    # filterset_class = dataFilter
    # filterset_fields = ('station')

    def get(self, request, *args, **kwargs):
        station = kwargs.get("station")
        if station is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request)

data_mixin_view = dataMixinView.as_view()

class statsMixinView(mixins.ListModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = weatherStats.objects.all()
    serializer_class = statSerializer
    # filterset_class = dataFilter
    # filterset_fields = ('station')

    def get(self, request, *args, **kwargs):
        station = kwargs.get("station")
        if station is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request)

stats_mixin_view = statsMixinView.as_view()
