import redis
from datetime import timedelta
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db

from resources.item import Item, ItemList
from resources.store import Store, StoreList
from security import identity, authenticate
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.article import Article, Articles
from blocklist import BLOCKLIST



ACCESS_EXPIRES = timedelta(hours=1)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = 'mositafa'

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()
    
# ====================================== JWT_CONFIG =========================================    
jwt  = JWTManager(app)

jwt_redis_blocklist = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin' : True}
    return {'is_admin' : False}

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'message' : 'The Token has expired',
        'error' : 'token_expired'
    }), 401
    
@jwt.invalid_token_loader
def invalid_token_clallback(error):
    return jsonify({
        'message' : 'Signature verification failed',
        'error' : 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missaing_token_callback(error):
    return jsonify({
        'description' : 'Request does not contain an access token',
        'error' : 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_refresh_callback():
    return jsonify({
        'description' : 'The Token is not fresh',
        'error' : 'fresh_token_required'
    }), 401
    
@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description' : 'The Token has been revoked',
        'error' : 'token_revoked'
    }), 401
    
# ====================================== END_OF JWT_CONFIG ========================================= 
    
    
# ============================= URL ==========================================    
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

api.add_resource(Article, '/article/<string:title>')
api.add_resource(Articles, '/articles')

api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

api.add_resource(TokenRefresh, '/refresh')
# ============================= END_OF_URL ==================================== 



if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
    



    
