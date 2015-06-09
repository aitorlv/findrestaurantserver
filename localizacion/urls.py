#-*- encoding: utf-8 -*-
from django.conf.urls import patterns, include, url
import localizacion
from localizacion import views
from django.contrib import admin
from django.contrib.auth.decorators import login_required
admin.autodiscover()
urlpatterns = patterns('',
                       url(r'^$', 'localizacion.views.inicio', name='inicio'),
                       url(r'^main/', 'localizacion.views.inicio', name='inicio'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'usuario/login.html'}),
                       url(r'^registro/$',views.Registro_Usuario.as_view(),name='registro'),
                       url(r'^registro_restaurante/$',login_required(views.Crear_Restaurante.as_view()),name='registro_restaurante'),
                       url(r'^lista_usuarios/$', login_required(views.UsuariosList.as_view()), name='usuarios_list'),
                       url(r'^lista_duenos/$', login_required(views.UsuariosListPorDuenos.as_view()), name='duenos_list'),
                       url(r'^lista/$', login_required(views.UsuariosListNormal.as_view()), name='normales_list'),
                       url(r'^lista_Restaurantes/$', login_required(views.RestauranteListNormal.as_view()), name='restaurantes_list'),
                       url(r'^mejor_valorados/$', login_required(views.MejorValorado.as_view()), name='mejor_valorados'),
                       url(r'^perfil/(?P<pk>\d+)$', login_required(views.UsuarioPerfil.as_view()), name='usuario_perfil'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'usuario/logout.html'}),
                       url(r'^editar/(?P<pk>\d+)$', login_required(views.UsuarioEdit.as_view()) , name='usuario_edit'),
                       url(r'^milocal/(?P<pk>\d+)$', login_required(views.MiLocal.as_view()) , name='milocal'),
                       url(r'^borrar/(?P<pk>\d+)$', login_required(views.UsuarioDelete.as_view()), name='usuario_delete'),
                       url(r'^cambiarpass/(?P<pk>\d+)$', login_required(views.CambiarPass.as_view()) , name='usuario_cambiar_pass'),
                       url(r'^misvaloraciones/(?P<pk>\d+)$', login_required(views.MisValoraciones.as_view()) , name='mis_valoraciones'),
                       url(r'^mimejorvaloracion/(?P<pk>\d+)$', login_required(views.MiMejorValoracion.as_view()) , name='mis_mejor_valoracion'),
                       url(r'^misvisitas/(?P<pk>\d+)$', login_required(views.MisVisitas.as_view()) , name='mis_visitas'),
                       url(r'^mismejorvisita/(?P<pk>\d+)$', login_required(views.MiMejorVisita.as_view()) , name='mis_mejor_visitas'),

                       url(r'^java/', include('localizacion.urls_java')),

    # (r'^time/$', current_datetime),
    # (r'^lista/$', lista_restaurantes),
)