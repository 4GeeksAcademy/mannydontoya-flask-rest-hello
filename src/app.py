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
from models import db, User, Character, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user/all', methods=['GET'])
def get_all_users():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users, 200)

@app.route('/user/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.json.get("user_id")
    if user_id is None:
        return jsonify({"message": "Please provide user ID"}), 400
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"message": "User not found"}), 404
    user_data = user.serialize()
    favorites = {
        "favorite_planets": user_data.get("favorite_planets", []),
        "favorite_characters": user_data.get("favorite_characters", [])
    }
    return jsonify(favorites), 200

# @app.route('/user/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     user = User.query.get(user_id)
#     return jsonify(user.serialize()), 200

# @app.route('/user', methods=['POST'])
# def createUser():
#     username = request.json["username"]
#     password = request.json["password"]
#     user1 = User(user_name=username, password=password)
#     db.session.add(user1)
#     db.session.commit()
#     response_body = {
#         "msg": f"Successfully created: {username}"
#     }

#     return jsonify(response_body), 200

@app.route('/favorites', methods=['POST'])
def create_fave():

    if request.json["category"] == "character":
        char = Character(
            name=request.json["name"],
            gender=request.json["gender"],
            birth_year=request.json["birth_year"],
            height=request.json["height"],
            mass=request.json["mass"]
        )
        db.session.add(char)


        fave = Favorite(
            name=request.json["name"],
            category=request.json["category"],
            user_id=request.json["user_id"],
            character_id=request.json["entity_id"]
        ) 
    elif request.json["category"] == "planet":
        planet = Planet(
            name=request.json["name"],
            climate=request.json["climate"],
            gravity=request.json["gravity"],
            population=request.json["population"],
            terrain=request.json["terrain"]
            )
        db.session.add
        fave = Favorite(
            name=request.json["name"],
            category=request.json["category"],
            user_id=request.json["user_id"],
            planet_id=request.json["entity_id"]
        ) 
    
    db.session.add(fave)
    db.session.commit()




    response_body = {
        "msg": f"Successfully created: {username}"
    }

    return jsonify(response_body), 200


@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters]), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"message": "Character not found"}), 404
    return jsonify(character.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"message": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.json.get("user_id")
    if user_id is None:
        return jsonify({"message": "Please provide user ID"}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"message": "Planet not found"}), 404
    user.favorite_planets.append(planet)
    db.session.commit()
    return jsonify({"message": "Favorite planet added"}), 201

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    user_id = request.json.get("user_id")
    if user_id is None:
        return jsonify({"message": "Please provide user ID"}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"message": "Character not found"}), 404
    user.favorite_characters.append(character)
    db.session.commit()
    return jsonify({"message": "Favorite character added"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.json.get("user_id")
    if user_id is None:
        return jsonify({"message": "Please provide user ID"}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"message": "Planet not found"}), 404
    if planet in user.favorite_planets:
        user.favorite_planets.remove(planet)
        db.session.commit()
        return jsonify({"message": "Favorite planet removed"}), 200
    return jsonify({"message": "Planet is not in favorites"}), 404

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    user_id = request.json.get("user_id")
    if user_id is None:
        return jsonify({"message": "Please provide user ID"}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"message": "Character not found"}), 404
    if character in user.favorite_characters:
        user.favorite_characters.remove(character)
        db.session.commit()
        return jsonify({"message": "Favorite character removed"}), 200
    return jsonify({"message": "Character is not in favorites"}), 404



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
