from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from blacklist import BLACKLIST
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserLogin, UserLogout, UserRegister
from flask import jsonify
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['JWT_SECRET_KEY'] = 'Dont TellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api=Api(app)

jwt=JWTManager(app)

@app.before_first_request
def cria_banco():
    banco.create_all()
    
@jwt.token_in_blocklist_loader

def verifica_blacklist(self,token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalido(jwt_header, jwt_payload):
    return jsonify({'message':'You have benn logged out'}), 401 # unauthorizad



api.add_resource(Hoteis,'/hoteis')
api.add_resource(Hotel,'/hoteis/<string:hotel_id>')
api.add_resource(User,'/usuarios/<int:user_id>')
api.add_resource(UserRegister,'/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)



#http://127.0.0.1:5000/hoteis
