from django import forms


class CalculationForm(forms.Form):
    tipo_calculo = forms.ChoiceField(choices=(('fisica', 'Pessoa física'), ('juridica', 'Pessoa jurídica')))
    energia = forms.DecimalField(required=False, min_value=0)
    transporte = forms.DecimalField(required=False, min_value=0)
    combustivel = forms.DecimalField(required=False, min_value=0)
    viagens = forms.DecimalField(required=False, min_value=0)
    agua = forms.DecimalField(required=False, min_value=0)
    residuos = forms.DecimalField(required=False, min_value=0)
    empresa = forms.CharField(required=False, max_length=150)
    funcionarios = forms.IntegerField(required=False, min_value=1)
    energia_pj = forms.DecimalField(required=False, min_value=0)
    gasolina_pj = forms.DecimalField(required=False, min_value=0)
    diesel_pj = forms.DecimalField(required=False, min_value=0)
    transporte_pj = forms.DecimalField(required=False, min_value=0)
    viagens_pj = forms.DecimalField(required=False, min_value=0)
    residuos_pj = forms.DecimalField(required=False, min_value=0)

    def clean(self):
        cleaned_data = super().clean()
        calculation_type = cleaned_data.get('tipo_calculo')
        if calculation_type == 'juridica':
            if not cleaned_data.get('empresa'):
                self.add_error('empresa', 'Informe o nome da empresa.')
            if not cleaned_data.get('funcionarios'):
                self.add_error('funcionarios', 'Informe a quantidade de funcionários.')
        return cleaned_data
