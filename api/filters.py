from django_filters import rest_framework as filters
from .models import weatherData, weatherStats


    
class dataFilter(filters.FilterSet):
    station = filters.ChoiceFilter(choices=[])
    year = filters.ChoiceFilter(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['station'].extra['choices'] = [(value, value) for value in weatherData.objects.values_list('station', flat=True).distinct().order_by('station')]
        self.filters['year'].extra['choices'] = [(value, value) for value in weatherData.objects.values_list('year', flat=True).distinct().order_by('year')]

    class Meta:
        model = weatherData
        fields = ['station','year']

class statFilter(filters.FilterSet):
    station = filters.ChoiceFilter(choices=[])
    year = filters.ChoiceFilter(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['station'].extra['choices'] = [(value, value) for value in weatherStats.objects.values_list('station', flat=True).distinct().order_by('station')]
        self.filters['year'].extra['choices'] = [(value, value) for value in weatherStats.objects.values_list('year', flat=True).distinct().order_by('year')]

    class Meta:
        model = weatherStats
        fields = ['station', 'year']