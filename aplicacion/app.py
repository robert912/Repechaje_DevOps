#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,click,json

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource
from aplicacion.config import app_config
from aplicacion.enviroment import env
from aplicacion.db import db
from aplicacion.redis import redis
from aplicacion.modelos import *

from tests.app_tests import Prueba
from aplicacion.helpers.sesion import Sesion
from aplicacion.recursos.login import Login
from aplicacion.recursos.Persona import PersonaResource, PersonaIdentificacion
from aplicacion.recursos.PdfGenerator import GeneratePdf


app = Flask(__name__)
CORS(app)

enviroment = "development"

app.config.from_object(app_config[enviroment])
db.init_app(app)
redis.init_app(app)
api = Api(app)


@app.before_request
def verifica_token():
    if request.method != 'OPTIONS' and request.endpoint != 'login' and request.endpoint != 'prueba':
        if not request.headers.get('Authorization'):
            return jsonify({'message': 'Acceso denegado'}), 403
        else:
            es_valido = Sesion.validar_token(request.headers.get('Authorization'))
            if es_valido == False:
                return jsonify({'message' :'Acceso denegado'}),403

api.add_resource(Prueba, '/prueba')
api.add_resource(Login, '/login')
api.add_resource(PersonaResource, '/getpersona')
api.add_resource(PersonaIdentificacion, '/personabyrut')
api.add_resource(GeneratePdf,'/generate_pdf')

app.run(host='0.0.0.0', port=5000)