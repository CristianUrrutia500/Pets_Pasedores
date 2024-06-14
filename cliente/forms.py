from django.contrib.auth.forms import UserCreationForm
from .models import Cliente, Mascota
from django import forms

# registrar cliente

class ClienteCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cliente
        fields = UserCreationForm.Meta.fields + (
            "edad",
            "comuna",
            "direccion",
            "telefono",
            "email",
            "first_name",
            "last_name",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.edad = self.cleaned_data["edad"]
        user.comuna = self.cleaned_data["comuna"]
        user.direccion = self.cleaned_data["direccion"]
        user.telefono = self.cleaned_data["telefono"]
        # user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# registrar mascota

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ["nombre", "edad", "foto","tamanno"]

# editar perfil

class ClienteUpdateForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["edad", "comuna", "direccion", "telefono", "first_name", "last_name"]

    def save(self, commit=True):
        cliente = super().save(commit=False)
        print("XDDDD")

        if commit:
            cliente.save()
        return cliente