from django.contrib import admin  # type: ignore[import-not-found]

from .models import Calculation, CalculationCompany, CalculationIndividual, Emission


admin.site.register(Calculation)
admin.site.register(CalculationIndividual)
admin.site.register(CalculationCompany)
admin.site.register(Emission)
