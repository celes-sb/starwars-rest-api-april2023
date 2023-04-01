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
from models import db, User, People, Planet, Vehicle
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

@app.route('/user', methods=['GET'])
def handle_hello():
    users = User.query.all()
    users = list((map(lambda item: item.serialize(), users)))
    print(users)
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(users), 200

@app.route('/register', methods=['POST'])
def register_user():
    #recibir body en json y almacenarl en la variable body
    body = request.get_json() #request.json() pero hay q importar request y json
    #ordernar campos recibidos
    email = body['email']
    name = body['name']
    password = body['password']
    is_active = body['is_active']
    
    #validaciones
    if body is None: #ejecuto una excepcion de la API
        raise APIException('You need to specify the request body as json object', status_code=400)
    
    if 'email' not in body:
        raise APIException('You need to specify the email', status_code=400)
    if 'name' not in body:
        raise APIException('You need to specify the name', status_code=400)
    if 'password' not in body:
        raise APIException('You need to specify the password', status_code=400)
    if 'is_active' not in body:
        raise APIException('You need to specify if user is active or not', status_code=400)
    
    #estructura para almacenar datos de usuarios nuevos
    #creada clase User en la variable new_user
    new_user = User(email=email, name=name, password=password, is_active=is_active)
    
    #comitear la sesión
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"mensaje": "Usuario creado correctamente"}), 201

@app.route('/get-user/<int:id>', methods=['GET'])
def get_specific_user(id):
    user = User.query.get(id)
    
    return jsonify(user.serialize()), 200

@app.route('/get-user', methods=['POST'])
def get_specific_user2():
    body = request.get_json()
    id = body['id']
    
    user = User.query.get(id)

    return jsonify(user.serialize()), 200 

@app.route('/get-user', methods=['DELETE'])
def delete_specific_user():
    body = request.get_json()
    id = body['id']
    
    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit

    return jsonify("Usuario borrado"), 200 

@app.route('/get-user', methods=['PUT'])
def edit_user():
    body = request.get_json()
    id = body['id']
    name = body["name"]

    user = User.query.get(id)
    user.name = name
    
    db.session.commit()

    return jsonify(user.serialize()), 200 

#APIS DE PEOPLE --------------------------------------------

@app.route('/get-people/<int:id>', methods=['GET'])
def get_specific_people(id):
    people = People.query.get(id)
    
    return jsonify(people.serialize()), 200

@app.route('/get-people', methods=['POST'])
def get_specific_people2():
    body = request.get_json()
    id = body['id']
    
    people = People.query.get(id)

    return jsonify(people.serialize()), 200 

@app.route('/get-people', methods=['DELETE'])
def delete_specific_people():
    body = request.get_json()
    id = body['id']
    
    people = People.query.get(id)

    db.session.delete(people)
    db.session.commit

    return jsonify("Person successfully deleted!"), 200 

@app.route('/get-people', methods=['PUT'])
def edit_people():
    body = request.get_json()
    id = body['id']
    name = body["name"]

    people = User.query.get(id)
    people.name = name
    
    db.session.commit()

    return jsonify(people.serialize()), 200 

#APIS DE PLANET --------------------------------------------

@app.route('/get-planet/<int:id>', methods=['GET'])
def get_specific_planet(id):
    planet = Planet.query.get(id)
    
    return jsonify(planet.serialize()), 200

@app.route('/get-planet', methods=['POST'])
def get_specific_planet2():
    body = request.get_json()
    id = body['id']
    
    planet = Planet.query.get(id)

    return jsonify(planet.serialize()), 200 

@app.route('/get-planet', methods=['DELETE'])
def delete_specific_planet():
    body = request.get_json()
    id = body['id']
    
    planet = Planet.query.get(id)

    db.session.delete(planet)
    db.session.commit

    return jsonify("Planet successfully deleted!"), 200 

@app.route('/get-planet', methods=['PUT'])
def edit_planet():
    body = request.get_json()
    id = body['id']
    name = body["name"]

    planet = Planet.query.get(id)
    planet.name = name
    
    db.session.commit()

    return jsonify(planet.serialize()), 200 

#APIS DE VEHICLE --------------------------------------------

@app.route('/get-vehicle/<int:id>', methods=['GET'])
def get_specific_vehicle(id):
    vehicle = Vehicle.query.get(id)
    
    return jsonify(vehicle.serialize()), 200

@app.route('/get-vehicle', methods=['POST'])
def get_specific_vehicle2():
    body = request.get_json()
    id = body['id']
    
    vehicle = Vehicle.query.get(id)

    return jsonify(vehicle.serialize()), 200 

@app.route('/get-vehicle', methods=['DELETE'])
def delete_specific_vehicle():
    body = request.get_json()
    id = body['id']
    
    vehicle = Vehicle.query.get(id)

    db.session.delete(vehicle)
    db.session.commit

    return jsonify("Vehicle successfully deleted!"), 200 

@app.route('/get-vehicle', methods=['PUT'])
def edit_vehicle():
    body = request.get_json()
    id = body['id']
    name = body["name"]

    vehicle = Vehicle.query.get(id)
    vehicle.name = name
    
    db.session.commit()

    return jsonify(vehicle.serialize()), 200 

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
