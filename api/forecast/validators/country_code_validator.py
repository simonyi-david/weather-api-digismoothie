from rest_framework.exceptions import ValidationError

from api.forecast.enums import CountryCode


class CountryCodeArgumentValidator:

    def __call__(self, country_code):
        if country_code not in CountryCode.values:
            raise ValidationError(f"Country code '{country_code}' not allowed.")

        return country_code
