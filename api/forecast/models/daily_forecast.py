from django.db.models import Model, CharField, DateField, DateTimeField, FloatField
from django.utils import timezone

from api.forecast.enums import CountryCode, TemperatureThreshold, TemperatureResultName
from api.forecast.helpers.datetime_functions import round_datetime_to_hours
from api.forecast.querysets.daily_forecast_queryset import DailyForecastQuerySet


class DailyForecast(Model):
    date = DateField()
    country_code = CharField(max_length=2, choices=CountryCode.choices)
    last_update_dt = DateTimeField(null=True, blank=True)
    average_temperature = FloatField()

    objects = DailyForecastQuerySet.as_manager()

    class Meta:
        ordering = ["-date"]
        unique_together = ["date", "country_code"]

    def __str__(self):
        return f"[{self.country_code}] {self.date} - {self.get_average_temperature_string()}"

    def save(self, *args, **kwargs):
        self.last_update_dt = round_datetime_to_hours(self.last_update_dt)
        super().save(*args, **kwargs)

    def get_average_temperature_string(self) -> str:
        if self.average_temperature > TemperatureThreshold.GOOD.value:
            return TemperatureResultName.GOOD
        elif self.average_temperature < TemperatureThreshold.BAD.value:
            return TemperatureResultName.BAD.value
        else:
            return TemperatureResultName.NORMAL.value

    def updated_in_last_hour(self) -> bool:
        now = timezone.now()
        rounded_now = round_datetime_to_hours(now)
        if rounded_now > self.last_update_dt:
            return False
        return True
