from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.forecast.handlers.weather_forecast_handler import WeatherForecastAPIHandler
from api.forecast.serializers import (
    WeatherForecastQueryParamsSerializer,
    WeatherForecastSerializer,
)


class WeatherForecastView(APIView):

    @swagger_auto_schema(query_serializer=WeatherForecastQueryParamsSerializer())
    def get(self, request, format=None):
        query_serializer = WeatherForecastQueryParamsSerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        forecast_api = WeatherForecastAPIHandler(
            target_date=query_serializer.validated_data["date"],
            country_code=query_serializer.validated_data["country_code"]
        )
        forecast = forecast_api.get_forecast()
        serializer = WeatherForecastSerializer(forecast)

        return Response(serializer.data, status=status.HTTP_200_OK)
