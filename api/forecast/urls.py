from django.urls import path

from api.forecast.views import WeatherForecastView

urlpatterns = [
    path("weather-forecast/", WeatherForecastView.as_view(), name="weather-forecast")
]
