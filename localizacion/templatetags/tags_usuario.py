__author__ = 'aitor'


from django import template
from localizacion.models import Usuario
register=template.Library()


@register.filter(name='get_tipo_usuario')
def get_tipo_usuario_por_dejangouser(user,arg):
    u=Usuario.objects.get(usuario_django=user)
    tipo=u.tipo
    return tipo==arg