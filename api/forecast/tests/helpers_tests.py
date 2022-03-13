from django.test import TestCase
from django.utils import timezone

from api.forecast.helpers.datetime_functions import round_datetime_to_hours, round_datetime_to_days


class HelpersTestCase(TestCase):

    def test_datetime_round_to_hours_none_dt(self):
        dt = None
        self.assertIsNone(round_datetime_to_hours(dt))

    def test_datetime_round_to_hours(self):
        dt = timezone.now()

        expected_dt = dt.replace(minute=0, second=0, microsecond=0)
        actual_dt = round_datetime_to_hours(dt)

        self.assertEqual(expected_dt, actual_dt)

    def test_round_datetime_to_days_none_dt(self):
        dt = None
        self.assertIsNone(round_datetime_to_days(dt))

    def test_round_datetime_to_days(self):
        dt = timezone.now()

        expected_dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        actual_dt = round_datetime_to_days(dt)

        self.assertEqual(expected_dt, actual_dt)
