from rest_framework.fields import SerializerMethodField, DateField
from rest_framework.serializers import ModelSerializer

from api.forecast.models import DailyForecast
from api.forecast.validators import ForecastDateValidator


class WeatherForecastSerializer(ModelSerializer):
    forecast = SerializerMethodField()

    class Meta:
        model = DailyForecast
        fields = ['forecast']

    def get_forecast(self, instance):
        return instance.get_average_temperature_string()


class WeatherForecastQueryParamsSerializer(ModelSerializer):
    date = DateField(validators=[ForecastDateValidator()])

    class Meta:
        model = DailyForecast
        fields = ["date", "country_code"]

    def get_unique_together_validators(self):
        """Overriding method to disable unique together checks"""
        return []
