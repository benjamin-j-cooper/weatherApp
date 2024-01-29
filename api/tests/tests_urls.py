from django.test import SimpleTestCase
from django.urls import reverse, resolve
from api.views import weather_Data_View, weather_Stats_View

class TestUrls(SimpleTestCase):

    def test_weather_url_is_resolved(self):
        url = reverse('weather')
        self.assertEqual(resolve(url).func.view_class, weather_Data_View)
    
    def test_stats_url_is_resolved(self):
        url = reverse('stats')
        self.assertEqual(resolve(url).func.view_class, weather_Stats_View)
