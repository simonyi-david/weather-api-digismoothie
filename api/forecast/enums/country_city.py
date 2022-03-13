from django.db.models import TextChoices

from api.core.enum_mixins import GetEnumByLabelMixin


class CountryCity(GetEnumByLabelMixin, TextChoices):
    CZ = "Brno"
    SK = "Bratislava"
    UK = "London"
