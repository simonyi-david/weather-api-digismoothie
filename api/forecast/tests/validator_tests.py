from datetime import date, timedelta

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from api.core.settings import MAX_FORECAST_DAYS, MAX_FORECAST_DAYS_API_CALL
from api.forecast.enums import CountryCode
from api.forecast.validators import CountryCodeArgumentValidator, ForecastDateValidator, ForecastDateArgumentValidator


class CountryCodeArgumentValidatorTestCase(TestCase):

    def setUp(self):
        self.validator = CountryCodeArgumentValidator()

    def test_country_code_validator(self):
        for country_code in CountryCode.values:
            self.assertEqual(country_code, self.validator(country_code))

    def test_country_code_validator_exception(self):
        self.assertRaises(ValidationError, self.validator, "US")
        self.assertRaises(ValidationError, self.validator, "CR")


class ForecastDateValidatorTestCase(TestCase):

    def setUp(self):
        self.validator = ForecastDateValidator()

    def test_yesterday_date(self):
        yesterday = date.today() - timedelta(days=1)
        self.assertRaises(ValidationError, self.validator, yesterday)

    def test_last_year_date(self):
        last_year = date.today() - timedelta(days=365)
        self.assertRaises(ValidationError, self.validator, last_year)

    def test_far_future_date(self):
        far_future = date.today() + timedelta(days=MAX_FORECAST_DAYS + 1)
        self.assertRaises(ValidationError, self.validator, far_future)

        far_future += timedelta(days=3)
        self.assertRaises(ValidationError, self.validator, far_future)

    def test_all_allowed_dates(self):
        for i in range(MAX_FORECAST_DAYS_API_CALL):
            test_date = date.today() + timedelta(days=i)
            self.assertEqual(test_date, self.validator(test_date))


class ForecastDateArgumentValidatorTestCase(TestCase):

    def setUp(self):
        self.validator = ForecastDateArgumentValidator()

    def test_wrong_format_dd_mm_yyyy_1(self):
        date_string = "13.3.2022"
        self.assertRaises(ValidationError, self.validator, date_string)

    def test_wrong_format_dd_mm_yyyy_2(self):
        date_string = "13/3/2022"
        self.assertRaises(ValidationError, self.validator, date_string)

    def test_wrong_format_dd_mm_yyyy_3(self):
        date_string = "13-3-2022"
        self.assertRaises(ValidationError, self.validator, date_string)

    def test_wrong_format_mm_dd_yyyy_1(self):
        date_string = "3.13.2022"
        self.assertRaises(ValidationError, self.validator, date_string)

    def test_wrong_format_mm_dd_yyyy_2(self):
        date_string = "3-13-2022"
        self.assertRaises(ValidationError, self.validator, date_string)

    def test_wrong_format_mm_dd_yyyy_3(self):
        date_string = "3/13/2022"
        self.assertRaises(ValidationError, self.validator, date_string)

    def test_wrong_format_yyyy_dd_mm_1(self):
        date_string = "2022.13.03"
        self.assertRaises(ValidationError, self.validator, date_string)

    def test_wrong_format_yyyy_dd_mm_2(self):
        date_string = "2022-13-03"
        self.assertRaises(ValidationError, self.validator, date_string)

    def test_wrong_format_yyyy_dd_mm_3(self):
        date_string = "2022/13/03"
        self.assertRaises(ValidationError, self.validator, date_string)

    def test_correct_format(self):
        date_string = "2022-03-13"
        expected_date = date(2022, 3, 13)
        actual_date = self.validator(date_string)

        self.assertEqual(expected_date, actual_date)
