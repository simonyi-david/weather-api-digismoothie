import argparse

from django.core.management import BaseCommand
from rest_framework.exceptions import ValidationError

from api.forecast.enums import CountryCode
from api.forecast.handlers.weather_forecast_handler import WeatherForecastAPIHandler
from api.forecast.validators import ForecastDateArgumentValidator, CountryCodeArgumentValidator


def date_validator(value):
    validator = ForecastDateArgumentValidator()
    try:
        value = validator(value)
    except ValidationError as e:
        raise argparse.ArgumentTypeError(e)

    return value


def country_code_validator(value):
    validator = CountryCodeArgumentValidator()

    try:
        validator(value)
    except ValidationError as e:
        raise argparse.ArgumentTypeError(e)

    return value


class Command(BaseCommand):
    help = "Gets forecast info for country and date"

    def add_arguments(self, parser):
        parser.add_argument("date", type=date_validator, help="Forecast date in format 'YYYY-MM-DD'")
        parser.add_argument(
            "country_code",
            type=country_code_validator,
            help=f"Get forecast for country based on ISO_CODE_2, choices {CountryCode.values}"
        )

    def handle(self, *args, **kwargs):
        target_date = kwargs["date"]
        country_code = kwargs["country_code"]

        forecast_api = WeatherForecastAPIHandler(target_date, country_code)
        forecast = forecast_api.get_forecast()

        return forecast.get_average_temperature_string()
