from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
@login_required
def calculations_api(request):

    if request.method == "GET":
        return JsonResponse({
            "success": True,
            "message": "API de cálculos funcionando."
        })

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "error": "Método não permitido."
            },
            status=405
        )

    try:
        data = json.loads(request.body)

    except json.JSONDecodeError:
        return JsonResponse(
            {
                "success": False,
                "error": "JSON inválido."
            },
            status=400
        )

    tipo = data.get("tipo")

    total = data.get("total")

    breakdown = data.get("breakdown", {})

    if tipo not in ["fisica", "juridica"]:
        return JsonResponse(
            {
                "success": False,
                "error": "Tipo de cálculo inválido."
            },
            status=400
        )

    if total is None:
        return JsonResponse(
            {
                "success": False,
                "error": "O campo total é obrigatório."
            },
            status=400
        )

    return JsonResponse(
        {
            "success": True,
            "message": "Cálculo recebido com sucesso.",
            "data": {
                "tipo": tipo,
                "total": total,
                "breakdown": breakdown,
                "user": request.user.username,
            }
        },
        status=201
    )