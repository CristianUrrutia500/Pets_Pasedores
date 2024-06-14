from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'El usuario no existe. Por favor, verifica tus credenciales.')
            return None
        
        if user.check_password(password):
            return user
        else:
            messages.error(request, 'Contraseña incorrecta. Por favor, verifica tus credenciales.')
            return None
