"""weather_forecast URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from api.forecast.urls import urlpatterns as forecast_urls

schema_view = get_schema_view(
   openapi.Info(
      title="Weather forecast API",
      default_version='v1',
      description="Weather forecast API test project for Digismoothie",
   ),
   public=True,
)


urlpatterns = [
    path("", include(forecast_urls)),
    path("admin/", admin.site.urls),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
