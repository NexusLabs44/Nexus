from django import forms
from django.contrib.auth import authenticate

from .models import User


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Senha',
        min_length=6,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='Confirmar senha',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('name', 'email', 'phone')
        labels = {
            'name': 'Nome completo',
            'email': 'E-mail',
            'phone': 'Telefone',
        }
        widgets = {
            'name': forms.TextInput,
            'email': forms.EmailInput,
            'phone': forms.TextInput,
        }

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise forms.ValidationError('As senhas não coincidem.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            self.user = authenticate(
                self.request,
                username=email.lower().strip(),
                password=password,
            )
            if self.user is None:
                raise forms.ValidationError('E-mail ou senha inválidos.')
            if not self.user.is_active:
                raise forms.ValidationError('Esta conta está desativada.')
        return cleaned_data
