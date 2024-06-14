from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2', 'edad')  # Incluye el campo 'edad' en el formulario de creación

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    verbose_name_plural = 'Usuarios'
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('edad','direccion','telefono','comuna')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'edad','email'),
        }),
    )

admin.site.register(User, CustomUserAdmin)


