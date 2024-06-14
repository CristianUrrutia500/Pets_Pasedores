# from django.contrib import admin
# from .models import Reserva
# from .forms import ReservaForm

# class ReservaAdmin(admin.ModelAdmin):
#     form = ReservaForm

#     def save_model(self, request, obj, form, change):
#         mascotas_seleccionadas = form.cleaned_data['mascotas']
#         horario_paseo = form.cleaned_data['horario_paseo']
        
#         for mascota in mascotas_seleccionadas:
#             # Crear una instancia de Reserva para cada mascota
#             reserva = Reserva(mascota=mascota, horario_paseo=horario_paseo)
#             reserva.save()

# admin.site.register(Reserva, ReservaAdmin)

from django.contrib import admin
from .models import Reserva
from .forms import ReservaForm, HorarioPaseo

class ReservaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Reserva, ReservaAdmin)

