from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from api.forecast.enums import CountryCode
from api.forecast.helpers.datetime_functions import round_datetime_to_hours
from api.forecast.models import DailyForecast


class DailyForecastQuerySetTestCase(TestCase):

    def setUp(self):
        self.date = "2022-03-14"
        average_temperature = 10.0
        current_dt = round_datetime_to_hours(timezone.now())
        outdated_dt = round_datetime_to_hours(timezone.now()) - timedelta(hours=1)

        DailyForecast.objects.create(
            date=self.date,
            average_temperature=average_temperature,
            last_update_dt=current_dt,
            country_code=CountryCode.CZ.value
        )
        DailyForecast.objects.create(
            date=self.date,
            average_temperature=average_temperature,
            last_update_dt=current_dt,
            country_code=CountryCode.SK.value
        )
        DailyForecast.objects.create(
            date=self.date,
            average_temperature=average_temperature,
            last_update_dt=outdated_dt,
            country_code=CountryCode.UK.value
        )

    def test_filter_country_forecast(self):
        expected_count = 1
        actual_count = DailyForecast.objects.filter_country_forecast(self.date, CountryCode.CZ.value).count()
        self.assertEqual(expected_count, actual_count)

        actual_count = DailyForecast.objects.filter_country_forecast(self.date, CountryCode.SK.value).count()
        self.assertEqual(expected_count, actual_count)

        actual_count = DailyForecast.objects.filter_country_forecast(self.date, CountryCode.UK.value).count()
        self.assertEqual(expected_count, actual_count)

    def test_exclude_outdated_forecast(self):
        expected_count = 2
        actual_count = DailyForecast.objects.exclude_outdated_forecast().count()
        self.assertEqual(expected_count, actual_count)

    def test_combined_filter_exclude_forecast(self):
        expected_count = 1
        actual_count = DailyForecast.objects\
            .filter_country_forecast(self.date, CountryCode.CZ.value)\
            .exclude_outdated_forecast()\
            .count()
        self.assertEqual(expected_count, actual_count)

        actual_count = DailyForecast.objects\
            .filter_country_forecast(self.date, CountryCode.SK.value)\
            .exclude_outdated_forecast()\
            .count()
        self.assertEqual(expected_count, actual_count)

        expected_count = 0
        actual_count = DailyForecast.objects\
            .filter_country_forecast(self.date, CountryCode.UK.value)\
            .exclude_outdated_forecast()\
            .count()
        self.assertEqual(expected_count, actual_count)
