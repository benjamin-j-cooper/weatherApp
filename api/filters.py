from django_filters import rest_framework as filters
from .models import weatherData, weatherStats

class dataFilter(filters.FilterSet):
    name = filters.MultipleChoiceFilter(lookup_expr='iexact')

    class Meta:
        model = weatherData
        fields = ['station', 'year']

class statFilter(filters.FilterSet):
    name = filters.MultipleChoiceFilter(lookup_expr='iexact')

    class Meta:
        model = weatherStats
        fields = ['station', 'year']