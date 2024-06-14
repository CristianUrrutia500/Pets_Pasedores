# reset/views.py

from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import View
from .forms import CustomPasswordResetForm  # Asegúrate de que la ruta de importación es correcta

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'reset/password_reset_form.html'
    success_url = reverse_lazy('index')  # Cambia 'index' al nombre correcto de tu vista de índice

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Hemos enviado un correo electrónico con instrucciones para restablecer su contraseña.")
        return response

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        messages.success(self.request, "Tu contraseña ha sido restablecida exitosamente.")
        return redirect('index')  # Cambia 'index' al nombre correcto de tu vista de índice