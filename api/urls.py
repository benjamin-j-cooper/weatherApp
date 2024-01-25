from django.urls import path, re_path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Weather Data Viewer API",
        default_version='v1',
        description="Welcome to Ben's Weather Data Viewer",
        terms_of_service="",
        contact=openapi.Contact(email="benjamin.cooper06@gmail.com"),
        license=openapi.License(name="Open Source"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('weather/', views.weather_view),  #localhost:8000/api/weather
    path('weather/stats/', views.stats_view), #localhost:8000/api/weather/stats
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]