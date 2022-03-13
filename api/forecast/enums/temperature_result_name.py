from django.db.models import TextChoices


class TemperatureResultName(TextChoices):
    GOOD = "good"
    NORMAL = "soso"
    BAD = "bad"
