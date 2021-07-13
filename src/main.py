"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personaje, Planet, FavPlanets, FavCharacters
import json
import datetime
## Nos permite hacer las encripciones de contraseñas
from werkzeug.security import generate_password_hash, check_password_hash

## Nos permite manejar tokens por authentication (usuarios) 
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def handle_hello():
    people_query = Personaje.query.all()
    all_people = list(map(lambda x: x.serialize(), people_query))
    # if user_query is None:
    #     return "Not found", 404
    
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "personajes": all_people
        
    }

    return jsonify(response_body), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_personaje(id):
    personaje = Personaje.query.get(id).serialize()
    # if user_query is None:
    #     return "Not found", 404
    print(personaje)
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "personaje": personaje
        
    }

    return jsonify(response_body), 200



@app.route('/planets/', methods=['GET'])
def get_planets():
    query_planets = Planet.query.all()
    query_planets = list(map(lambda x: x.serialize(), query_planets))
    
    # if user_query is None:
    #     return "Not found", 404
    print(query_planets)
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "planets": query_planets
        
    }

    return jsonify(response_body), 200

@app.route('/users/', methods=['GET'])
def get_todos_usuarios():
    query_users = User.query.all()
    query_users = list(map(lambda x: x.serialize(), query_users))
    
    # if user_query is None:
    #     return "Not found", 404
    print(query_users)
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "usuarios": query_users
        
    }

    return jsonify(response_body), 200

@app.route('/register', methods=['POST'])
def register():
 if request.method == 'POST':
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    username = request.json.get("username", None)
    
    if not email:
        return "Email required", 401
    username = request.json.get("username", None)
    if not username:
        return "Username required", 401
    password = request.json.get("password", None)
    if not password:
        return "Password required", 401

    email_query = User.query.filter_by(email=email).first()
    if email_query:
        return "This email has been already taken", 401
    
    user = User()
    user.email = email
    user.is_active= True
    user.username = username
    hashed_password = generate_password_hash(password)
    user.password = hashed_password
    
    db.session.add(user)
    db.session.commit()

    response = {
        "msg": "Added successfully",
        "username": username
    }
    return jsonify(response), 200


@app.route('/login', methods=['POST'])
def login():
    
    email = request.json.get("email")
    password = request.json.get("password")

    if not email:
        return jsonify({"msg":"Email required"}), 400

    if not password:
        return jsonify({"msg":"Password required"}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"msg": "The email is not correct"}), 401
    if not check_password_hash(user.password, password):
         return jsonify({"msg": "The password is not correct"}), 401

    expiracion = datetime.timedelta(days=3)
    access_token = create_access_token(identity=user.email, expires_delta=expiracion)

    data = {
            "user": user.serialize(),
            "token": access_token,
            "expires": expiracion.total_seconds()*1000,
            "userId": user.id
        }


    return jsonify(data), 200 

@app.route('/planet/<int:id>', methods=['GET'])
def get_planet(id):
    planet = Planet.query.get(id)
    if planet is None:
        return "Planet not found", 404
    planet = planet.serialize()
    print(planet)
    # if user_query is None:
    #     return "Not found", 404
    print(planet)
    response_body = {
       
        "planet": planet
        
    }

    return jsonify(response_body), 200   



@app.route('/users/<int:user_id>/favorites', methods=["GET"])
@jwt_required() #Private space
def get_favorites_by_user(user_id):
    token = get_jwt_identity()
    user_query = User.query.get(user_id)
    user_planets = user_query.favorites()['planets']
    # if not user_planets:
    #     return jsonify("ERROR"), 404
    user_characters = user_query.favorites()['characters']
    # if not user_characters:
    #     return jsonify("ERROR"), 404
    user_planets = list(map(lambda x: x.serialize(), user_planets))
    user_characters = list(map(lambda x: x.serialize(), user_characters))
    
    if user_query is None:
        return "Planet not found", 404
    
    if user_query is None:
        return "Not found", 404
    response_body = {
        "fav_planets": user_planets,
        "fav_characters": user_characters,
        "user": token
    }
    

    return jsonify(response_body), 200
    # return jsonify('200'), 200
    


@app.route('/users/<int:user_id>/favorites', methods=['POST'])
@jwt_required() #Private space
def post_favorite(user_id):
    token = get_jwt_identity()
    body = request.get_json()
    if body["type"].lower() == "planeta":
        fav = FavPlanets(typeOfFav=body['type'], userId=body['userId'], planetId=body['planetId'], name= body['name'])
        db.session.add(fav)
        db.session.commit()
        response_body = {
       
        "State": "Added",
        "user": token
        
    }
    elif body["type"].lower() == "personaje":
        fav = FavCharacters(typeOfFav=body['type'], userId=body['userId'], characterId=body['characterId'], name= body['name'])
        db.session.add(fav)
        db.session.commit()
        response_body = {
       
        "State": "Added",
        "user": token
        }
    

    return jsonify("Ok"), 200


@app.route('/users/<int:user_id>/favorites/', methods=["DELETE"])
@jwt_required() #Private space
def delete_fav(user_id):
    token = get_jwt_identity()
    user = User.query.get(user_id)
    character_id = request.json.get('character_id')
    planet_id = request.json.get('planet_id')

    if not character_id and not planet_id:
        return "Request is empty", 400
    
    if character_id:
        char = FavCharacters.query.filter_by(userId=user_id, characterId=character_id).first()
        print(char)
        db.session.delete(char)
        db.session.commit()
        return "Ok", 200

    if planet_id:
        char = FavPlanets.query.filter_by(userId=user_id, planetId=planet_id).first()
        print(char)
        db.session.delete(char)
        db.session.commit()
        return "Ok", 200
    return "Ok", 200
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
