from django.conf import settings
from django.db import models


class Calculation(models.Model):
    class CalculationType(models.TextChoices):
        INDIVIDUAL = 'individual', 'Pessoa fisica'
        COMPANY = 'company', 'Pessoa juridica'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_column='idUsuario',
        on_delete=models.CASCADE,
        related_name='calculations',
    )
    id = models.AutoField(primary_key=True, db_column='idCalculo')
    date_calc = models.DateTimeField(null=True, db_column='dataCalculo')
    type_calc = models.CharField(max_length=30, choices=CalculationType.choices, db_column='tipoCalculo')

    class Meta:
        db_table = 'Calculo'
        managed = False
        ordering = ['-date_calc']

    @property
    def total_emissions(self):
        return sum((emission.emission_value for emission in self.emissions.all()), 0)

    def __str__(self):
        return f'{self.get_type_calc_display()} - {self.date_calc:%d/%m/%Y}'


class CalculationIndividual(models.Model):
    calculation = models.OneToOneField(
        Calculation,
        db_column='idCalculoPessoa',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='individual_details',
    )
    travels_plane = models.DecimalField(max_digits=10, decimal_places=2, null=True, db_column='viagensAviao')
    energy = models.DecimalField(max_digits=10, decimal_places=2, null=True, db_column='energia')
    fuel = models.DecimalField(max_digits=10, decimal_places=2, null=True, db_column='combustivel')
    transport = models.DecimalField(max_digits=10, decimal_places=2, null=True, db_column='transporte')
    water = models.DecimalField(max_digits=10, decimal_places=2, null=True, db_column='agua')
    waste = models.DecimalField(max_digits=10, decimal_places=2, null=True, db_column='residuos')

    class Meta:
        db_table = 'CalculoPessoa'
        managed = False


class CalculationCompany(models.Model):
    calculation = models.OneToOneField(
        Calculation,
        db_column='idCalculoEmpresa',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='company_details',
    )
    name_company = models.CharField(max_length=150, db_column='nomeEmpresa')
    num_employee = models.PositiveIntegerField(null=True, db_column='numeroFuncionarios')
    energy = models.DecimalField(max_digits=10, decimal_places=2, null=True, db_column='energia')
    gasoline = models.DecimalField(max_digits=10, decimal_places=2, null=True, db_column='gasolina')
    transport_fleet = models.DecimalField(max_digits=10, decimal_places=2, null=True, db_column='frotaTransporte')
    diesel = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    travels_corporate = models.DecimalField(max_digits=10, decimal_places=2, null=True, db_column='viagensCorporativas')
    waste = models.DecimalField(max_digits=10, decimal_places=2, null=True, db_column='residuos')

    class Meta:
        db_table = 'CalculoEmpresa'
        managed = False


class Emission(models.Model):
    calculation = models.ForeignKey(
        Calculation,
        db_column='idCalculo',
        on_delete=models.CASCADE,
        related_name='emissions',
    )
    id = models.AutoField(primary_key=True, db_column='idEmissao')
    category = models.CharField(max_length=100, db_column='categoria')
    emission_value = models.DecimalField(max_digits=12, decimal_places=2, db_column='valorEmissao')
    emission_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, db_column='percentualEmissao')

    class Meta:
        db_table = 'Emissao'
        managed = False
        ordering = ['-emission_value']

    def __str__(self):
        return f'{self.category} - {self.emission_value}'
