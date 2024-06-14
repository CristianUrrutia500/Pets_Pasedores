from django.contrib.auth.models import Group

def grupo_usuario(request):
    grupo_usuario = None
    if request.user.is_authenticated:
        if request.user.groups.filter(name='cliente').exists():
            grupo_usuario = 'cliente'
        elif request.user.groups.filter(name='paseador').exists():
            grupo_usuario = 'paseador'
    
    return {'grupo_usuario': grupo_usuario}
