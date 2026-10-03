from django.urls import path

from .api_views import (
api_login,
api_logout,
api_me,
api_register,
)

urlpatterns = [
path("login/", api_login, name="api_login"),
path("register/", api_register, name="api_register"),
path("logout/", api_logout, name="api_logout"),
path("me/", api_me, name="api_me"),
]