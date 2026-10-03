from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CalculationForm
from .models import Calculation, CalculationCompany, CalculationIndividual, Emission


def _number(value):
    if value in (None, ''):
        return Decimal('0')
    return Decimal(str(value))


def _calculation_payload(calculation):
    breakdown = {}
    for emission in calculation.emissions.all():
        breakdown[emission.category] = float(emission.emission_value)
    total = sum(breakdown.values())
    return {
        'tipo': 'juridica' if calculation.type_calc == 'company' else 'fisica',
        'total': round(total),
        'breakdown': breakdown,
        'date': calculation.date_calc.isoformat() if calculation.date_calc else '',
    }


def _save_calculation(user, data):
    is_company = data['tipo_calculo'] == 'juridica'
    calculation_type = 'company' if is_company else 'individual'

    if is_company:
        energy = _number(data.get('energia_pj'))
        gasoline = _number(data.get('gasolina_pj'))
        diesel = _number(data.get('diesel_pj'))
        fleet = _number(data.get('transporte_pj'))
        travel = _number(data.get('viagens_pj'))
        waste = _number(data.get('residuos_pj'))
        breakdown = {
            'energia': energy * Decimal('0.0817') * 12,
            'combustivel': gasoline * Decimal('2.31') * 12 + diesel * Decimal('2.68') * 12,
            'transporte': fleet * Decimal('0.21') * 12,
            'viagens': travel * 90,
            'residuos': waste * Decimal('2.5') * 52,
        }
    else:
        energy = _number(data.get('energia'))
        transport = _number(data.get('transporte'))
        fuel = _number(data.get('combustivel'))
        travel = _number(data.get('viagens'))
        water = _number(data.get('agua'))
        waste = _number(data.get('residuos'))
        breakdown = {
            'energia': energy * Decimal('0.0817') * 12,
            'transporte': transport * Decimal('0.21') * 52,
            'combustivel': fuel * Decimal('2.31') * 12,
            'viagens': travel * 90,
            'agua': water * Decimal('0.000298') * 365,
            'residuos': waste * Decimal('2.5') * 52,
        }

    with transaction.atomic():
        calculation = Calculation.objects.create(
            user=user,
            date_calc=timezone.now(),
            type_calc=calculation_type,
        )
        if is_company:
            CalculationCompany.objects.create(
                calculation=calculation,
                name_company=data['empresa'],
                num_employee=data['funcionarios'],
                energy=energy,
                gasoline=gasoline,
                transport_fleet=fleet,
                diesel=diesel,
                travels_corporate=travel,
                waste=waste,
            )
        else:
            CalculationIndividual.objects.create(
                calculation=calculation,
                travels_plane=travel,
                energy=energy,
                fuel=fuel,
                transport=transport,
                water=water,
                waste=waste,
            )
        total = sum(breakdown.values())
        for category, value in breakdown.items():
            Emission.objects.create(
                calculation=calculation,
                category=category,
                emission_value=value,
                emission_percentage=(value / total * 100) if total else 0,
            )
    return calculation


@login_required
def home_view(request):
    return render(request, 'index.html')


@login_required
def calculator_view(request):
    form = CalculationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        calculation = _save_calculation(request.user, form.cleaned_data)
        return redirect(f'/resultados/?calculo={calculation.pk}')
    return render(request, 'calculadora.html', {'form': form})


@login_required
def profile_view(request):
    calculations = Calculation.objects.filter(user=request.user).prefetch_related('emissions')[:20]
    history = [_calculation_payload(calculation) for calculation in calculations]
    return render(request, 'profile.html', {
        'dashboard_user': {'name': request.user.name, 'email': request.user.email},
        'dashboard_history': history,
    })


@login_required
def results_view(request):
    calculation_id = request.GET.get('calculo')
    if calculation_id:
        calculation = get_object_or_404(Calculation, pk=calculation_id, user=request.user)
    else:
        calculation = Calculation.objects.filter(user=request.user).prefetch_related('emissions').first()
    result = _calculation_payload(calculation) if calculation else None
    return render(request, 'resultados.html', {'calculation_result': result})
