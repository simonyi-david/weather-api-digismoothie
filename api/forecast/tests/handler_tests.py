from datetime import date, timedelta
from unittest import mock

from django.test import TestCase

from api.forecast.enums import CountryCode
from api.forecast.handlers.weather_forecast_handler import WeatherForecastAPIHandler
from api.forecast.models import DailyForecast
from api.forecast.serializers import WeatherApiResponseSerializer
from api.forecast.tests.expected_response import LONDON_DICT_RESPONSE


class WeatherForecastAPIHandlerTestCase(TestCase):

    @mock.patch('api.forecast.handlers.WeatherForecastAPIHandler._call_weather_api')
    def test_call_weather_api(self, mock_get):
        serializer = WeatherApiResponseSerializer(data=LONDON_DICT_RESPONSE)
        serializer.is_valid()

        mock_get.return_value = serializer.validated_data

        target_date = date.today()
        country_code = CountryCode.CZ.value
        api = WeatherForecastAPIHandler(target_date, country_code)

        empty_count = DailyForecast.objects.all().count()
        self.assertEqual(0, empty_count)

        actual_result = api.get_forecast()
        expected_result = DailyForecast.objects.filter_country_forecast(target_date, country_code).get()
        self.assertEqual(expected_result, actual_result)

        expected_count = 3
        actual_count = DailyForecast.objects.all().count()
        self.assertEqual(expected_count, actual_count)

        tomorrow_date = target_date + timedelta(days=1)
        api.target_date = tomorrow_date

        expected_result = DailyForecast.objects.filter_country_forecast(tomorrow_date, country_code).get()
        actual_result = api.get_forecast()
        self.assertEqual(expected_result, actual_result)
        mock_get.assert_called_once()
