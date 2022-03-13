from datetime import date, timedelta

from rest_framework.exceptions import ValidationError
from rest_framework.fields import DateField

from api.core.settings import MAX_FORECAST_DAYS


class ForecastDateArgumentValidator(DateField):

    def __call__(self, date_value):
        date_value = self.to_internal_value(date_value)
        validator = ForecastDateValidator()
        return validator(date_value)


class ForecastDateValidator:

    def __call__(self, date_value):
        current_date = date.today()
        if date_value < current_date:
            raise ValidationError(f"Date has to be greater or same as current date: {current_date}")

        date_delta = date_value - current_date
        if date_delta.days > MAX_FORECAST_DAYS:
            furthest_allowed_date = current_date + timedelta(days=MAX_FORECAST_DAYS)
            raise ValidationError(f"Furthest allowed forecast date is: {furthest_allowed_date}")

        return date_value
