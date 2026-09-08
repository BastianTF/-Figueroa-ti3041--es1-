from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class RegistroCorreoForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con este correo electrónico.')
        return email

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.email = self.cleaned_data['email']
        usuario.username = self.cleaned_data['email']
        if commit:
            usuario.save()
        return usuario


class InicioCorreoForm(AuthenticationForm):
    username = forms.EmailField(label='Correo electrónico')

    def clean(self):
        correo = self.cleaned_data.get('username', '').strip().lower()
        password = self.cleaned_data.get('password')
        usuario = User.objects.filter(email__iexact=correo).first()
        username = usuario.username if usuario else correo
        self.user_cache = authenticate(self.request, username=username, password=password)
        if self.user_cache is None:
            raise forms.ValidationError('El correo electrónico o la contraseña no son correctos.')
        self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data
