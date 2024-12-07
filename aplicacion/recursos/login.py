import sys, os
from flask_restful import Resource, reqparse

from aplicacion.modelos.Usuario import Usuario
from aplicacion.helpers.sesion import Sesion

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('usuario', type=str, required=True, help="El usuario es requerido")
        parser.add_argument('password', type=str, required=True, help="La contraseña es requerida")
        
        data = parser.parse_args()
        try:
            user = Usuario.get_by_usuario(data['usuario'])
            passw = Usuario.getHash(data['password'])
            if user and 'password_hash' in user[0] and user[0]['password_hash'] == passw:
                tokenId = Sesion.generar_tokenid(user[0]['usuario'], user[0]['password_hash'], 'Admin')
                return {"access_token": tokenId}, 200
            return {"message": "usuario o contraseña incorrectos"}, 401
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500