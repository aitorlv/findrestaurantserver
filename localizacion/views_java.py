# -*- encoding: utf-8 -*-
__author__ = 'aitor'
from  localizacion.models import Restaurantes,Usuario,RestaurantesVisitados,Tokenregister
import django.http as http
import pdb
from django.views.decorators.csrf import csrf_exempt
import json
import django.contrib.auth as auth
from annoying.functions import get_object_or_None
from utilidades import Token
import datetime
from django.contrib.auth.models import User

'''
definicion para conseguir el usuario de django a partir del token
'''
def get_userdjango_by_token(datos):
    token = datos.get('token')
    user_token = Tokenregister.objects.get(token=token)
    return user_token.user


'''
definicion para conseguir el usuario de django a partir del id de usuario
'''
def get_userdjango_by_id(datos):
    userdjango_id = datos.get('usuario_id')
    userdjango = get_object_or_None(User, pk=userdjango_id)
    return userdjango


'''
definicion para conseguir el usuario de la aplicacion a partir del token
'''
def get_usuario_by_token(datos):
    token = datos.get('token')
    user_token = Tokenregister.objects.get(token=token)
    usuario = Usuario.objects.get(usuario_django=user_token.user)
    return usuario


'''
definicion para comprobar el usuario
'''
def comprobar_usuario(datos):
    userdjango = get_userdjango_by_id(datos)
    user_token = get_userdjango_by_token(datos)

    if (user_token is not None) and (userdjango is not None):
        if user_token == userdjango:
            return True
        else:
            return False


'''
definicion para logear un usuario desde la aplicación java
'''
@csrf_exempt
def loginMovil(request):
    print "Login"
    try:

        datos= json.loads(request.POST['data'])
        us = datos.get('usuario').lower()
        password = datos.get('password')

        if (us is None and password is None) or (us == "" and password == ""):
            response_data = {'result': 'error', 'message': 'Falta el usuario y el password'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if us is None or us == "" :
            response_data = {'result': 'error', 'message': 'Falta el usuario'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if password is None or password == "":
            response_data = {'result': 'error', 'message': 'Falta el password'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        user = auth.authenticate(username=us, password=password)

        if user is not None:
            if user.is_active:
                user_token = get_object_or_None(Tokenregister,user=user)
                if user_token==None:
                    token1 = str(user.id) + "_" + Token.id_generator()
                    tokenform = Tokenregister(token=token1, user=user)
                    tokenform.save()
                    user_token = get_object_or_None(Tokenregister, user=user)
                else:
                    user_token.date = datetime.datetime.now()
                    user_token.token = str(user.id) + "_" + Token.id_generator()
                    user_token.save()
                usuario = Usuario.objects.get(usuario_django=user)
                response_data = {'result': 'ok', 'message': 'Usuario logeado', 'token':user_token.token, 'usuario':user.username}

                usuario.conectado = True
                usuario.save()
                return http.HttpResponse(json.dumps(response_data), content_type="application/json")

            else:
                response_data = {'result': 'error', 'message': 'Usuario no activo'}
                return http.HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data = {'result': 'error', 'message': 'Usuario no válido'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'E0007', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


'''
registro de usuario
'''

@csrf_exempt
def registrarUsuario(request):
    try:
        datos= json.loads(request.POST['data'])
        print datos
        usuario = datos.get('usuario').lower()
        password = datos.get('password')
        tipo = datos.get('tipo')
        if usuario is not None:
            comprobacionusuario = User.objects.filter(username=usuario)
            if comprobacionusuario.count()==0:
                userDjango = User(username=usuario)
                userDjango.set_password(password)
                userDjango.save()
                usuarioApp = Usuario(usuario_django=userDjango, tipo=tipo)
                usuarioApp.save()
                response_data = {'result': 'ok', 'message': 'Usuario registrado correctamente.', 'usuario':usuario}
                return http.HttpResponse(json.dumps(response_data), content_type="application/json")

            else:
                response_data = {'result': 'error', 'message': 'Usuario existente'}
                return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        else:
            response_data = {'result': 'error', 'message': 'Error al enviar el usuario'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'E0002', 'result': 'error', 'message': 'Error en registro de usuario: '+str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


'''
logout
otro que devueva todos los rest, insertar puntuacion, visitas realizadas.
'''
@csrf_exempt
def logout(request):
    print "Logout"
    try:
        datos = json.loads(request.POST['data'])
        if comprobar_usuario(datos):
            userdjango = get_userdjango_by_token(datos)
            usuario = get_usuario_by_token(datos)
            user_token = get_object_or_None(Tokenregister, user=userdjango)
            if user_token is None:
                response_data = {'result': 'ok', 'message': 'Usuario  deslogueado'}
            else:
                usuario.conectado = False
                usuario.save()
                user_token.delete()
                response_data = {'result': 'ok', 'message': 'Usuario ya deslogueado'}
        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'E0005', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

'''
def para devolver todos los restaurantes
'''
@csrf_exempt
def devolverRestaurantes(request):
    try:
        datos = json.loads(request.POST['data'])
        if comprobar_usuario(datos):
           restaurantes=Restaurantes.objects.all();
           response_data = {'result': 'ok', 'message': 'Descarga Restaurantes', 'restaurantes': []}
           for rest in restaurantes:
                response_data['restaurantes'].append({'nombre': rest.nombre,
                                                         'direccion': rest.direccion,
                                                         'longitud': rest.longitud,
                                                         'latitud':rest.latitud,
                                                         'tiporestaurante':rest.tiporestaurante,
                                                         'valoracion':rest.valoracion})
        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'E0005', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

'''
def para insertar puntuacion
'''
@csrf_exempt
def insertarPuntuacion(request):
    try:
        datos = json.loads(request.POST['data'])
        if comprobar_usuario(datos):
            usuario_id = datos.get("usuario_id")
            restaurante_id=datos.get("restaurante_id")
            restaurante=get_object_or_None(Restaurantes,pk=restaurante_id)
            valoracion=datos.get("valoracion",0)
            visitado=RestaurantesVisitados(restaurante=restaurante,id_usuario=usuario_id,valoracion=valoracion)
            visitado.save()
            todos=RestaurantesVisitados.objects.filter(restaurante=restaurante)
            media=restaurante.valoracion
            for t in todos:
                media=(media+t.valoracion)/2
            restaurante.valoracion=media
            restaurante.save()
            response_data = {'result': 'ok', 'message': 'Insertar valoracion'}
        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'E0005', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

'''
def visitas realizadas
'''
@csrf_exempt
def devolverVisitados(request):
    try:
        pdb.set_trace()
        datos = json.loads(request.POST['data'])
        if comprobar_usuario(datos):
           usuario_id=datos.get("usuario_id")
           visitados=RestaurantesVisitados.objects.all().filter(id_usuario=usuario_id);
           response_data = {'result': 'ok', 'message': 'Descarga visitados', 'visitados': []}
           for vist in visitados:
                response_data['visitados'].append({'id_usuario': vist.id_usuario,
                                                         'restaurante':{'nombre': vist.restaurante.nombre,
                                                         'direccion': vist.restaurante.direccion,
                                                         'longitud': vist.restaurante.longitud,
                                                         'latitud':vist.restaurante.latitud,
                                                         'tiporestaurante':vist.restaurante.tiporestaurante,
                                                         'valoracion':vist.restaurante.valoracion},
                                                         'valoracion': vist.valoracion})

        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'E0005', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")