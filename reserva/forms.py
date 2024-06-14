from django import forms
from .models import Reserva
from cliente.models import Mascota
from paseador.models import HorarioPaseo
from django.forms import DateInput

class ReservaForm(forms.ModelForm):
    def __init__(self, user=None, horarios_disponibles=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mascotas"].queryset = Mascota.objects.filter(duenno=user)

        # Filtrar las opciones del campo horario_paseo
        if horarios_disponibles is not None:
            self.fields["horario_paseo"].queryset = horarios_disponibles

            # Agrupar y ordenar los horarios por día de la semana y hora de inicio
            dias_ordenados = {'lunes': 1, 'martes': 2, 'miercoles': 3, 'jueves': 4, 'viernes': 5, 'sabado': 6, 'domingo': 7}
            horarios_ordenados = sorted(horarios_disponibles, key=lambda x: (dias_ordenados[x.dia.lower()], x.hora_inicio))
            choices = []
            for horario in horarios_ordenados:
                choices.append((horario.id, f"{horario.dia} - {horario.hora_inicio} - {horario.hora_fin}"))
            self.fields["horario_paseo"].choices = choices

    mascotas = forms.ModelMultipleChoiceField(
        queryset=Mascota.objects.none(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Reserva
        fields = ["mascotas", "horario_paseo", "fecha_paseo"]
        widgets = {
            'fecha_paseo': DateInput(attrs={'type': 'date'})
        }
