#-*- encoding: utf-8 -*-
__author__ = 'aitor'

import floppyforms as forms
from .models import *

class UsuarioRegistro(forms.ModelForm):
    TIPO = ((0, ("Dueño local")),(1, ("Cliente")))
    tipo = forms.ChoiceField(choices=TIPO)
    class Meta:
        model = Usuario

        exclude = {
            'conectado',
            'usuario_django'
        }


class RestauranteRegistro(forms.ModelForm):
     TIPO = ((0, ("Alta cocina")),(1, ("Buffet")),(2, ("Comida rapida")),(3,('Tematicos')))
     tiporestaurante=forms.ChoiceField(choices=TIPO)
     class Meta:
        model = Restaurantes

        exclude = {
            'usuario',
            'valoracion'
        }


class UsuarioUpdateForm(forms.ModelForm):
    error_css_class = 'alert alert-danger'
    usuario=forms.CharField()
    TIPO = ((0, ("Dueño local")),(1, ("Cliente")))
    tipo = forms.ChoiceField(choices=TIPO)

    class Meta:
        model = Usuario

        exclude = {
            'conectado',
            'usuario_django'
        }

class CambiarContrasenaForm(forms.Form):
    antigua = forms.CharField(widget=forms.PasswordInput, label='Contraseña Antigua')
    nueva = forms.CharField(widget=forms.PasswordInput, label='Contraseña Nueva')
    renueva = forms.CharField(widget=forms.PasswordInput, label='Repetir Contraseña Nueva')


class ContrasenaForm(forms.Form):
    contrasena = forms.CharField(widget=forms.PasswordInput, label='Contraseña')