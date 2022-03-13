from rest_framework.fields import FloatField, DateField, ListField
from rest_framework.serializers import Serializer


class ForecastDataSerializer(Serializer):
    avgtemp_c = FloatField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ForecastDaySerializer(Serializer):
    date = DateField()
    day = ForecastDataSerializer()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ForecastSerializer(Serializer):
    forecastday = ListField(child=ForecastDaySerializer())

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class WeatherApiResponseSerializer(Serializer):
    forecast = ForecastSerializer()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
