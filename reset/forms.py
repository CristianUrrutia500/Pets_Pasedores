# reset/forms.py

from django import forms
from django.contrib.auth.forms import PasswordResetForm
from usuario.models import User  # Importa tu modelo de usuario personalizado

class CustomPasswordResetForm(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No hay ninguna cuenta registrada con este correo electrónico.")
        return email
