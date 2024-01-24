from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_home), #localhost:8000/api/
    path('weather/', views.weather), #localhost:8000/api/
    path('', views.stats), #localhost:8000/api/
    # path('', views.dataCreateAPIView.as_view()),
    # path('<str:station>/', views.dataDetailAPIView.as_view()),
    # path('<>', views.stats),
]