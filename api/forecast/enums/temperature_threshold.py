from django.db.models import IntegerChoices


class TemperatureThreshold(IntegerChoices):
    GOOD = 20
    BAD = 10
