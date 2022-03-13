from datetime import datetime

from django.db import IntegrityError
from django.test import TestCase

from api.forecast.enums import CountryCode, TemperatureResultName
from api.forecast.models import DailyForecast


class DailyForecastTestCase(TestCase):

    def _create_forecast(self, date, country_code, average_temperature=10.0):
        return DailyForecast.objects.create(
            date=date,
            country_code=country_code,
            average_temperature=average_temperature
        )

    def test_only_unique_forecasts_exception(self):
        self._create_forecast(
            date="2022-01-01",
            country_code=CountryCode.CZ.value,
        )
        self.assertRaises(
            IntegrityError,
            DailyForecast.objects.create,
            date="2022-01-01",
            country_code=CountryCode.CZ.value,
            average_temperature=9.5
        )

    def test_create_multiple_forecasts_same_day(self):
        self._create_forecast("2022-03-10", CountryCode.CZ.value)
        self._create_forecast("2022-03-10", CountryCode.UK.value)
        self._create_forecast("2022-03-10", CountryCode.SK.value)

        expected_count = 3
        actual_count = DailyForecast.objects.all().count()
        self.assertEqual(expected_count, actual_count)

    def test_updated_dt_rounding(self):
        updated_dt = datetime(2022, 3, 13, 10, 6, 55)
        forecast = DailyForecast(
            date="2022-03-13",
            country_code=CountryCode.CZ.value,
            average_temperature=10.0,
            last_update_dt=updated_dt
        )
        forecast.save()
        expected_last_updated_dt = updated_dt.replace(minute=0, second=0)
        self.assertEqual(expected_last_updated_dt, forecast.last_update_dt)

    def test_forecast_string_output(self):
        forecast = self._create_forecast("2022-03-10", CountryCode.CZ.value, -7.9)
        self.assertEqual(TemperatureResultName.BAD.value, forecast.get_average_temperature_string())

        forecast.average_temperature = 9.9
        self.assertEqual(TemperatureResultName.BAD.value, forecast.get_average_temperature_string())

        forecast.average_temperature = 10.0
        self.assertEqual(TemperatureResultName.NORMAL.value, forecast.get_average_temperature_string())

        forecast.average_temperature = 15.5
        self.assertEqual(TemperatureResultName.NORMAL.value, forecast.get_average_temperature_string())

        forecast.average_temperature = 19.9
        self.assertEqual(TemperatureResultName.NORMAL.value, forecast.get_average_temperature_string())

        forecast.average_temperature = 20.1
        self.assertEqual(TemperatureResultName.GOOD.value, forecast.get_average_temperature_string())

        forecast.average_temperature = 26.6
        self.assertEqual(TemperatureResultName.GOOD.value, forecast.get_average_temperature_string())
