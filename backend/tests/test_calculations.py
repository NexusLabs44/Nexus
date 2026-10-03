from datetime import datetime
from types import SimpleNamespace

from django.test import SimpleTestCase
from django.utils import timezone

from calculations.forms import CalculationForm
from calculations.views import _calculation_payload, _number


class CalculationFormTests(SimpleTestCase):
    def test_individual_calculation_accepts_numeric_inputs(self):
        form = CalculationForm(data={
            'tipo_calculo': 'fisica',
            'energia': '10',
            'transporte': '5',
            'combustivel': '3',
            'viagens': '2',
            'agua': '100',
            'residuos': '1',
        })

        self.assertTrue(form.is_valid())

    def test_company_calculation_requires_company_fields(self):
        form = CalculationForm(data={'tipo_calculo': 'juridica'})

        self.assertFalse(form.is_valid())
        self.assertIn('empresa', form.errors)
        self.assertIn('funcionarios', form.errors)

    def test_negative_values_are_rejected(self):
        form = CalculationForm(data={
            'tipo_calculo': 'fisica',
            'energia': '-1',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('energia', form.errors)


class CalculationPayloadTests(SimpleTestCase):
    def test_number_converts_empty_values_to_zero(self):
        self.assertEqual(_number(''), 0)
        self.assertEqual(_number(None), 0)
        self.assertEqual(_number('2.5'), 2.5)

    def test_payload_sums_emissions_and_identifies_calculation_type(self):
        calculation = SimpleNamespace(
            type_calc='individual',
            date_calc=timezone.make_aware(datetime(2026, 1, 2)),
            emissions=SimpleNamespace(all=lambda: [
                SimpleNamespace(category='energia', emission_value=1.25),
                SimpleNamespace(category='transporte', emission_value=2),
            ]),
        )

        payload = _calculation_payload(calculation)

        self.assertEqual(payload['tipo'], 'fisica')
        self.assertEqual(payload['total'], 3)
        self.assertEqual(payload['breakdown'], {'energia': 1.25, 'transporte': 2.0})
        self.assertEqual(payload['date'], '2026-01-02T00:00:00-03:00')