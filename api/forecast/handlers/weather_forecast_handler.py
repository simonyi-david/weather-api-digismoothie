import json

import requests
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from api.core.settings import WEATHER_API_FORECAST_URL, WEATHER_API_KEY, MAX_FORECAST_DAYS_API_CALL
from api.forecast.enums.country_coordinates import CountryCoordinates
from api.forecast.exceptions import SiteUnreachable
from api.forecast.helpers.datetime_functions import round_datetime_to_hours
from api.forecast.models import DailyForecast
from api.forecast.serializers import WeatherApiResponseSerializer


class WeatherForecastAPIHandler:

    def __init__(self, target_date, country_code):
        self.target_date = target_date
        self.country_code = country_code

    def _call_weather_api(self):
        lat, lon = CountryCoordinates.get_by_label(self.country_code)
        try:
            response = requests.get(
                WEATHER_API_FORECAST_URL,
                params={
                    "key": WEATHER_API_KEY,
                    "q": f"{lat},{lon}",
                    "days": MAX_FORECAST_DAYS_API_CALL,
                    "aqi": "no",
                    "alerts": "no"
                }
            )
        except TimeoutError as e:
            raise e

        serializer = WeatherApiResponseSerializer(data=json.loads(response.text))
        if not serializer.is_valid():
            raise ValidationError({"message": "Failed to parse weatherapi.com data", "errors": serializer.errors})
        return serializer.validated_data

    def update_and_get_forecast(self):
        try:
            data = self._call_weather_api()
        except TimeoutError:
            '''When the site is unreachable try to get already saved forecast, otherwise raise error'''
            forecast = DailyForecast.objects.filter_country_forecast(self.target_date, self.country_code)
            if forecast.exists():
                return forecast.get()

            msg = (f"Forecast site {WEATHER_API_FORECAST_URL} is unreachable and "
                   f"no forecast for date {self.target_date} is present")
            raise SiteUnreachable(msg)

        with transaction.atomic():
            update_dt = timezone.now()
            rounded_update_dt = round_datetime_to_hours(update_dt)
            create_forecasts = []

            for day_data in data["forecast"]["forecastday"]:
                date = day_data["date"]
                average_temperature = day_data["day"]["avgtemp_c"]

                forecast = DailyForecast.objects.filter_country_forecast(date, self.country_code)
                if forecast.exists():
                    forecast.update(
                        average_temperature=average_temperature,
                        last_update_dt=rounded_update_dt
                    )
                else:
                    new_forecast = DailyForecast(
                        date=date,
                        country_code=self.country_code,
                        average_temperature=average_temperature,
                        last_update_dt=rounded_update_dt
                    )
                    create_forecasts.append(new_forecast)

            DailyForecast.objects.bulk_create(create_forecasts)

        return DailyForecast.objects\
            .filter_country_forecast(country_code=self.country_code, date=self.target_date)\
            .get()

    def get_forecast(self):
        forecast_qs = DailyForecast.objects.filter_country_forecast(self.target_date, self.country_code)

        up_to_date_forecast_qs = forecast_qs.exclude_outdated_forecast()
        if up_to_date_forecast_qs.exists():
            return up_to_date_forecast_qs.get()

        return self.update_and_get_forecast()
