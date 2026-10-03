from django.urls import path

from .api_views import calculations_api


urlpatterns = [
    path("", calculations_api, name="calculations_api"),
]