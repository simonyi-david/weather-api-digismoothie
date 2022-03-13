from enum import Enum

from api.core.enum_mixins import GetEnumByLabelMixin


class CountryCoordinates(GetEnumByLabelMixin, Enum):
    CZ = ("49.2", "16.63")
    SK = ("48.15", "17.12")
    UK = ("51.52", "-0.11")
