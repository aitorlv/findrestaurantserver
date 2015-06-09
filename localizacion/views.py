#-*- encoding: utf-8 -*-
__author__ = 'aitor'
import datetime

from django.http import HttpResponse
from django.views.generic import ListView, FormView, DeleteView,CreateView,UpdateView
from  localizacion.models import Restaurantes,Usuario,RestaurantesVisitados
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
import django.http as http
import forms
import models
import pdb
from django.db.models import Max

@login_required()
def inicio(request):
    usuario = Usuario.objects.get(usuario_django=request.user)
    return render_to_response('principal.html',context_instance=RequestContext(request,{'usuario':usuario}))


class Registro_Usuario(FormView):
    template_name = 'usuario/usuario_create.html'
    form_class = forms.UsuarioRegistro
    second_form_class = UserCreationForm

    def get(self, request, *args, **kwargs):
        usuario = self.form_class(initial=self.initial)
        django_usuario = self.second_form_class(initial=self.initial)
        return render(request, self.template_name, {'usuario':usuario,'django_usaurio':django_usuario })

    def post(self, request, *args, **kwargs):
        data = request
        usuario=forms.UsuarioRegistro(data.POST, data.FILES)
        django_usuario=UserCreationForm(data.POST)
        if django_usuario.is_valid() and usuario.is_valid():
            django=django_usuario.save()
            user=usuario.save(commit=False)
            user.usuario_django=django
            user.save()
            django.save()

            return render(request,'registro_Confirmado.html',{'mensaje':'Registrado con exito'})
        else:
            return render(request, self.template_name, {'usuario':usuario,'django_usaurio':django_usuario,"mal":"usuario no registrado" })



class UsuarioPerfil(CreateView):
    model = Restaurantes
    context_object_name = 'restaurantes'
    template_name = 'usuario/usuario_perfil.html'

    def get(self, request, *args, **kwargs):

        usuario = get_object_or_404(models.Usuario, pk=self.kwargs['pk'])
        restaurante= models.Restaurantes.objects.filter(usuario=usuario.usuario_django)
        return render(request, self.template_name, {'restaurantes':restaurante,'usuario': usuario})

class UsuarioEdit(FormView):
    template_name = 'usuario/usuario_edit.html'
    form_class = forms. UsuarioUpdateForm
    second_form_class = UserCreationForm

    def get(self, request, *args, **kwargs):
        usuario= get_object_or_404(models.Usuario, pk=self.kwargs['pk'])
        usuarioform = self.form_class(initial={'tipo':usuario.tipo,'usuario':usuario.usuario_django}, instance=usuario)
        return render(request, self.template_name, {'usuarioform': usuarioform,'usuario':usuario})

    def post(self, request, *args, **kwargs):
        data = request
        usuario = get_object_or_404(models.Usuario, pk=self.kwargs['pk'])
        usuarioform = self.form_class(data.POST,instance=usuario)

        if usuarioform.is_valid():

            djangouser =usuario.usuario_django

            nuevousuario = usuarioform['usuario'].value()
            djangouser.username = nuevousuario
            djangouser.save()

            return http.HttpResponseRedirect(reverse('usuario_perfil', args=(usuario.pk,)))

        return render(request, self.template_name, {'usuarioform': usuarioform, 'usuario': usuario})


class UsuarioDelete(DeleteView):
    template_name = 'usuario/usuario_delete.html'
    form_class = forms.ContrasenaForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        usuario = get_object_or_404(models.Usuario, pk=self.kwargs['pk'])
        return render(request, self.template_name, {'usuario': usuario, 'form':form})

    def post(self, request, *args, **kwargs):
        usuario = get_object_or_404(models.Usuario, pk=self.kwargs['pk'])
        djangouser = usuario.usuario_django
        form = self.form_class(request.POST)
        password = form['contrasena'].value()
        correcto = request.user.check_password(password)
        if correcto:
            if djangouser.pk == 1:
                return http.HttpResponseRedirect(reverse('usuarios_list'))
            else:
                djangouser.delete()
                return http.HttpResponseRedirect(reverse('usuarios_list'))

        else:
            return render(request, self.template_name, {'usuario': usuario ,'form':form})

# METODOS PARA LISTAR LOS DATOS  TANTO USUARIOS COMO RESTAURANTES

class UsuariosList(ListView):

    model = Usuario
    context_object_name = 'usuarios'
    template_name = 'usuario/usuarios_list.html'


    def get_queryset(self):
        by_id = Usuario.objects.all().order_by('id')

        return by_id

class UsuariosListPorDuenos(ListView):

    model = Usuario
    context_object_name = 'usuarios'
    template_name = 'usuario/usuarios_list.html'


    def get_queryset(self):
        by_id = Usuario.objects.all().filter(tipo = 0).order_by('id')

        return by_id


class UsuariosListNormal(ListView):

    model = Usuario
    context_object_name = 'usuarios'
    template_name = 'usuario/usuarios_list.html'


    def get_queryset(self):
        by_id = Usuario.objects.all().filter(tipo = 1).order_by('id')

        return by_id

class RestauranteListNormal(ListView):

    model = Restaurantes
    context_object_name = 'restaurantes'
    template_name = 'restaurantes/restaurantes_list.html'


    def get_queryset(self):
        by_id = Restaurantes.objects.all().order_by('tiporestaurante')

        return by_id

class MejorValorado(ListView):

    model = Restaurantes
    context_object_name = 'restaurantes'
    template_name = 'restaurantes/restaurantes_list.html'


    def get_queryset(self):
        by_id = Restaurantes.objects.all().filter(valoracion__gt= 7)

        return by_id


class MiLocal(ListView):

    model = Restaurantes
    context_object_name = 'restaurantes'
    template_name = 'restaurantes/restaurantes_list.html'

    def get(self, request, *args, **kwargs):
        user=get_object_or_404(models.Usuario,pk=self.kwargs['pk'])
        restaurantes= models.Restaurantes.objects.filter(usuario=user)
        return render(request, self.template_name, {'restaurantes':restaurantes, 'usuario':user})

class MisValoraciones(ListView):

    model = RestaurantesVisitados
    context_object_name = 'restaurantesvisitados'
    template_name = 'visitados/valoracion_list.html'

    def get(self, request, *args, **kwargs):
        user=get_object_or_404(models.Usuario,pk=self.kwargs['pk'])
        valoraciones= models.RestaurantesVisitados.objects.filter(id_usuario=user.pk)
        return render(request, self.template_name, {'valoraciones':valoraciones, 'usuario':user})

class MiMejorValoracion(ListView):

    model = RestaurantesVisitados
    context_object_name = 'restaurantesvisitados'
    template_name = 'visitados/valoracion_list.html'

    def get(self, request, *args, **kwargs):
        user=get_object_or_404(models.Usuario,pk=self.kwargs['pk'])
        max_val=models.RestaurantesVisitados.objects.filter(id_usuario=user.pk).aggregate(Max('valoracion'))
        valoraciones=models.RestaurantesVisitados.objects.filter(id_usuario=user.pk,valoracion=max_val['valoracion__max'])
        return render(request, self.template_name, {'valoraciones':valoraciones,'usuario':user})

class MisVisitas(ListView):

    model = RestaurantesVisitados
    context_object_name = 'restaurantesvisitados'
    template_name = 'visitados/mapa_list.html'

    def get(self, request, *args, **kwargs):
        user=get_object_or_404(models.Usuario,pk=self.kwargs['pk'])
        restaurantes= models.Restaurantes.objects.filter(usuario=user)
        valoraciones=models.RestaurantesVisitados.objects.filter(id_usuario=user.pk)
        return render(request, self.template_name, {'valoraciones':valoraciones,'usuario':user})

class MiMejorVisita(ListView):

    model = RestaurantesVisitados
    context_object_name = 'restaurantesvisitados'
    template_name = 'visitados/mapa_list.html'

    def get(self, request, *args, **kwargs):
        user=get_object_or_404(models.Usuario,pk=self.kwargs['pk'])
        max_val=models.RestaurantesVisitados.objects.filter(id_usuario=user.pk).aggregate(Max('valoracion'))
        valoraciones=models.RestaurantesVisitados.objects.filter(id_usuario=user.pk,valoracion=max_val['valoracion__max'])
        return render(request, self.template_name, {'valoraciones':valoraciones,'usuario':user})


class CambiarPass(FormView):
    template_name = 'usuario/cambiar_pass.html'
    form_class = forms.CambiarContrasenaForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        usuario = get_object_or_404(models.Usuario, pk=self.kwargs['pk'])
        return render(request, self.template_name, {'usuario': usuario,'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        usuario = get_object_or_404(models.Usuario, pk=self.kwargs['pk'])

        djangouser = usuario.usuario_django
        if form.is_valid():
            antigua = form['antigua'].value()
            nueva = form['nueva'].value()
            renueva = form['renueva'].value()
            correcto = request.user.check_password(antigua)
            if correcto:
                if nueva == renueva:
                    djangouser.set_password(nueva)
                    djangouser.save()
                    return http.HttpResponseRedirect(reverse('usuario_perfil', args=(usuario.pk,)))
                else:
                    men = "Las contraseñas no coinciden."
                    return render(request, self.template_name, {'usuario': usuario,'form':form, 'mensaje':men})
            else:
                men = "La contraseña antigua no es correcta. "
                return render(request, self.template_name, {'usuario': usuario,'form':form, 'mensaje':men})

        return render(request, self.template_name, {'usuario': usuario,'form':form})


# CLASES PARA LOS RESTAURANTES
class Crear_Restaurante(FormView):
    template_name = 'restaurantes/registro_restaurante.html'
    form_class = forms.RestauranteRegistro

    def get(self, request, *args, **kwargs):
        restaurante_form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'restaurante_form':restaurante_form})

    def post(self, request, *args, **kwargs):
        data = request
        restauranteform=forms.RestauranteRegistro(data.POST)
        django_usuario=request.user
        if restauranteform.is_valid():
            restaurante=restauranteform.save(commit=False)
            restaurante.usuario=django_usuario
            restaurante.valoracion=0
            restaurante.save()

            return render(request,'registro_Confirmado.html',{'mensaje':'Registrado con exito','restaurante':'restaurante'})
        else:
            return render(request, self.template_name, {'restaurante_form':restauranteform,"mal":"Registro no realizado" })

