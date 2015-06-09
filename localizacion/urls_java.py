# -*- encoding: utf-8 -*-
__author__ = 'aitor'
from django.conf.urls import patterns,url
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('', url(r'^loginMovil/$', 'localizacion.views_java.loginMovil'),
                       url(r'^logout/$', 'localizacion.views_java.logout'),
                       url(r'^registro/$', 'localizacion.views_java.registrarUsuario'),
                       url(r'^get_restaurantes/$', 'localizacion.views_java.devolverRestaurantes'),
                       url(r'^insertarValoracion/$', 'localizacion.views_java.insertarPuntuacion'),
                       url(r'^visitasRealizadas/$', 'localizacion.views_java.devolverVisitados'),
                       )