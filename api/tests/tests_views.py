from django.test import TestCase, Client
from django.urls import reverse
# from api.views import weather_Data_View, weather_Stats_View


class TestViews(TestCase):

    def setup(self):
        self.client = Client()

    def test_weather_list_get(self):
        # specify view
        url = reverse('weather')
        # Make a GET request to the view
        response = self.client.get(url)
        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

    def test_stats_list_get(self):
        # specify view
        url = reverse('stats')
        # Make a GET request to the view
        response = self.client.get(url)
        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)