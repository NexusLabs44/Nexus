from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('profile')

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    form = LoginForm(request, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.user)
        return redirect('profile')

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
