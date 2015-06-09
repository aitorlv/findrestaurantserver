# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Tokenregister(models.Model):
    user    = models.ForeignKey(User)
    token   = models.CharField(max_length=80)
    date    = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s" % self.tokenid

class Usuario(models.Model):
    usuario_django=models.ForeignKey(User)
    tipo = models.IntegerField(db_column='Tipo') # Field name made lowercase.
    conectado = models.BooleanField(default=False)
    def __unicode__(self):
        return u"%s" % self.usuario_django.username


class Restaurantes(models.Model):
    usuario = models.ForeignKey(User) # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=100) # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50) # Field name made lowercase.
    longitud = models.FloatField(db_column='Longitud') # Field name made lowercase.
    latitud = models.FloatField(db_column='Latitud') # Field name made lowercase.
    tiporestaurante = models.CharField(db_column='TipoRestaurante', max_length=100) # Field name made lowercase.
    valoracion = models.IntegerField(db_column='Valoracion') # Field name made lowercase.

class RestaurantesVisitados(models.Model):
    id_usuario = models.IntegerField(db_column='Id_Usuario') # Field name made lowercase.
    restaurante = models.ForeignKey(Restaurantes, db_column='Id_Restaurante') # Field name made lowercase.
    valoracion = models.IntegerField(db_column='Valoracion') # Field name made lowercase.




