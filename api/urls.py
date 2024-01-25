from django.urls import path
from . import views

urlpatterns = [
    # path('', views.api, name='home'),
    # path('weather/', views.weather), #localhost:8000/api/weather
    # path('weather/stats/', views.stats), #localhost:8000/api/weather/stats
    path('weather/', views.data_list_view), #localhost:8000/api/weather
    path('weather/stats/', views.stats_list_view), #localhost:8000/api/weather/stats
    # path('weather/', views.data_mixin_view),  #localhost:8000/api/weather
    # path('weather/stats/', views.stats_mixin_view), #localhost:8000/api/weather/stats

]