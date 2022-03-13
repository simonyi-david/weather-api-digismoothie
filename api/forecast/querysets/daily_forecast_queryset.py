from django.db.models import QuerySet
from django.utils import timezone

from api.forecast.helpers.datetime_functions import round_datetime_to_hours


class DailyForecastQuerySet(QuerySet):

    def filter_country_forecast(self, date, country_code):
        return self.filter(date=date, country_code=country_code)

    def exclude_outdated_forecast(self):
        now = timezone.now()
        rounded_now = round_datetime_to_hours(now)
        return self.exclude(last_update_dt__lt=rounded_now)
