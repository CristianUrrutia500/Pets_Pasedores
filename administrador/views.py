from django.shortcuts import render
from .forms import ContactoForm
from django.contrib import messages
# Create your views here.


def contact(request):
    data = {
        "form": ContactoForm(),
    }
    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Mensaje enviado correctamente. Nos pondremos en contacto contigo')
        else:
            data['form'] = formulario

    return render(request, "navegacion/contact.html", data)
