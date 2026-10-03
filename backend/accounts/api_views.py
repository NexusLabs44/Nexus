import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User


def _json_body(request):
    try:
        return json.loads(request.body or "{}")
    except (json.JSONDecodeError, TypeError):
        return None


def _user_data(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
    }


@csrf_exempt
def api_login(request):
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "error": "Método não permitido.",
        }, status=405)

    data = _json_body(request)

    if data is None:
        return JsonResponse({
            "success": False,
            "error": "JSON inválido.",
        }, status=400)

    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if not email or not password:
        return JsonResponse({
            "success": False,
            "error": "E-mail e senha são obrigatórios.",
        }, status=400)

    user = authenticate(
        request,
        username=email,
        password=password,
    )

    if user is None:
        return JsonResponse({
            "success": False,
            "error": "E-mail ou senha incorretos.",
        }, status=401)

    if not user.is_active:
        return JsonResponse({
            "success": False,
            "error": "Esta conta está desativada.",
        }, status=403)

    login(request, user)

    return JsonResponse({
        "success": True,
        "authenticated": True,
        "message": "Login realizado com sucesso.",
        "user": _user_data(user),
    })


@csrf_exempt
def api_register(request):
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "error": "Método não permitido.",
        }, status=405)

    data = _json_body(request)

    if data is None:
        return JsonResponse({
            "success": False,
            "error": "JSON inválido.",
        }, status=400)

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    phone = str(data.get("phone", "")).strip()

    password = str(
        data.get(
            "password1",
            data.get("password", ""),
        )
    )

    password2 = str(data.get("password2", ""))

    errors = {}

    if not name:
        errors["name"] = ["Informe seu nome completo."]

    if not email:
        errors["email"] = ["Informe seu e-mail."]

    if not password:
        errors["password1"] = ["Informe uma senha."]
    elif len(password) < 8:
        errors["password1"] = [
            "A senha deve possuir pelo menos 8 caracteres."
        ]

    if password != password2:
        errors["password2"] = [
            "As senhas não coincidem."
        ]

    if email and User.objects.filter(email=email).exists():
        errors["email"] = [
            "Este e-mail já está cadastrado."
        ]

    if errors:
        return JsonResponse({
            "success": False,
            "error": "Verifique os dados informados.",
            "errors": errors,
        }, status=400)

    try:
        user = User.objects.create_user(
            email=email,
            password=password,
            name=name,
            phone=phone or None,
        )
    except Exception:
        return JsonResponse({
            "success": False,
            "error": "Não foi possível criar a conta.",
        }, status=500)

    login(request, user)

    return JsonResponse({
        "success": True,
        "authenticated": True,
        "message": "Conta criada com sucesso.",
        "user": _user_data(user),
    }, status=201)


@login_required
def api_me(request):
    if request.method != "GET":
        return JsonResponse({
            "success": False,
            "error": "Método não permitido.",
        }, status=405)

    return JsonResponse({
        "success": True,
        "authenticated": True,
        "user": _user_data(request.user),
    })


@csrf_exempt
@login_required
def api_logout(request):
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "error": "Método não permitido.",
        }, status=405)

    logout(request)

    return JsonResponse({
        "success": True,
        "authenticated": False,
        "message": "Logout realizado com sucesso.",
    })
