from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from accounts.views import login_view, logout_view, register_view
from calculations.views import calculator_view, home_view, profile_view, results_view


urlpatterns = [
    path('', home_view, name='home'),
    path('calculadora/', calculator_view, name='calculator'),
    path('login/', login_view, name='login'),
    path('cadastro/', register_view, name='register'),
    path('perfil/', profile_view, name='profile'),
    path('resultados/', results_view, name='results'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
