"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


@app.route('/user', methods=['GET'])
def list_users():

    users = User.query.all()

    if users:
        return jsonify({
            "success": True,
            "data": [user.serialize() for user in users]
        }), 200
    else:
        return jsonify({
            "success": False,
            "msg": "No existen usuarios"
        }), 200


@app.route('/user/favorites', methods=['GET'])
@jwt_required()
def get_user_favorites():
    current_user_id = get_jwt_identity()

    favorites = Favorite.query.filter_by(user_id=current_user_id).all()

    if favorites:
        return jsonify({
            "success": True,
            "data": [favorite.serialize() for favorite in favorites]
        }), 200
    else:
        return jsonify({
            "success": False,
            "data": "No tiene favoritos agregados"
        }), 200


@app.route('/people', methods=['GET'])
def list_people():

    people = People.query.all()

    if people:
        return jsonify({
            "success": True,
            "data": [person.serialize() for person in people]
        }), 200
    else:
        return jsonify({
            "success": False,
            "msg": "No hay registro de personajes"
        }), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):

    people = db.session.get(People, people_id)

    if people:
        return jsonify({
            "success": True,
            "data": people
        }), 200
    else:
        return jsonify({
            "success": False,
            "msg": "No existe el personaje"
        }), 200


@app.route('/planets', methods=['GET'])
def list_planets():

    planets = Planet.query.all()

    if planets:
        return jsonify({
            "success": True,
            "data": [p.serialize() for p in planets]
        }), 200
    else:
        return jsonify({
            "success": False,
            "msg": "No hay registro de planetas"
        }), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):

    planet = db.session.get(Planet, planet_id)

    if planet:
        return jsonify({
            "success": True,
            "data": planet
        }), 200
    else:
        return jsonify({
            "success": False,
            "msg": "No existe el planeta"
        }), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
@jwt_required()
def add_planet_to_favorite(planet_id):

    current_user_id = get_jwt_identity()

    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({
            "success": False,
            "msg": "Planeta no encontrado"
        }), 200

    favorites_exists = Favorite.query.filter_by(
        user_id=current_user_id,
        element_id=planet_id,
        type="planet"
    ).first()

    if favorites_exists:
        return jsonify({
            "success": True,
            "msg": "El planeta ya está en favoritos"
        }), 200

    new_favorite = Favorite(
        user_id=current_user_id,
        element_id=planet_id,
        type="planet"
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({
        "success": True,
        "data": new_favorite.serialize()
    }), 201


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
@jwt_required()
def add_people_to_favorite(people_id):

    current_user_id = get_jwt_identity()

    people = People.query.get(people_id)

    if not people:
        return jsonify({
            "success": False,
            "msg": "Personaje no encontrado"
        }), 200

    favorites_exists = Favorite.query.filter_by(
        user_id=current_user_id,
        element_id=people_id,
        type="people"
    ).first()

    if favorites_exists:
        return jsonify({
            "success": True,
            "msg": "El personake ya está en favoritos"
        }), 200

    new_favorite = Favorite(
        user_id=current_user_id,
        element_id=people_id,
        type="people"
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({
        "success": True,
        "data": new_favorite.serialize()
    }), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
@jwt_required()
def delete_planet_favorite(planet_id):

    current_user_id = get_jwt_identity()

    favorite = Favorite.query.filter_by(
        user_id=current_user_id,
        element_id=planet_id,
        type="planet"
    ).first()

    if not favorite:
        return jsonify({
            "success": False,
            "msg": "Este planeta no está en favoritos"
        }), 200

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({
        "success": True,
        "msg": "Planeta eliminado de favoritos"
    }), 200


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
@jwt_required()
def delete_people_favorite(people_id):

    current_user_id = get_jwt_identity()

    favorite = Favorite.query.filter_by(
        user_id=current_user_id,
        element_id=people_id,
        type="people"
    ).first()

    if not favorite:
        return jsonify({
            "success": False,
            "msg": "Este personaje no está en favoritos"
        }), 200

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({
        "success": True,
        "msg": "Personaje eliminado de favoritos"
    }), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
