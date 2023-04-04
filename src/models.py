from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #nullable=False significa que no se puede dejar en blanco
    #unique=True, que no se puede repetir
    password = db.Column(db.String(250), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    favorite_people = db.relationship('FavoritePeople', backref = 'user', lazy=True)
    favorite_vehicle = db.relationship('FavoriteVehicle', backref = 'user', lazy=True)
    favorite_planet = db.relationship('FavoritePlanet', backref = 'user', lazy=True)
    
    #cambia la ubicacion de la memoria
    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    mass = db.Column(db.Integer, unique=False, nullable=False)
    height = db.Column(db.Integer, unique=False, nullable=False)
    hair_color = db.Column(db.String(50), unique=False, nullable=False)
    skin_color = db.Column(db.String(50), unique=False, nullable=False)
    eye_color = db.Column(db.String(50), unique=False, nullable=False)
    birth_year = db.Column(db.String(50), unique=False, nullable=False)
    gender = db.Column(db.String(50), unique=False, nullable=False)
    favorite_people = db.relationship('FavoritePeople', backref = 'people', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "mass": self.mass,
            "height": self.height,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender
            # do not serialize the password, its a security breach
        }

class FavoritePeople(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "people_name": People.query.get(self.people_id).serialize()["name"],
            "user_name": User.query.get(self.user_id).serialize()["name"],
            "user": User.query.get(self.user_id).serialize(),
            "people": People.query.get(self.people_id).serialize()
        }
#recomendacion separar los favoritos en tablas distintas
# new_favorite = FavoritePeople(user_id = db.Column....., )
# new_favorite.user -> obtengo toda la info del usuario q tiene a ese favorito en su lista y tmb obtengo sus metodos (serialize)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    model = db.Column(db.String(50), unique=False, nullable=False)
    manufacturer = db.Column(db.String(100), unique=False, nullable=False)
    cost_in_credits = db.Column(db.Integer, unique=False, nullable=False)
    length = db.Column(db.Integer, unique=False, nullable=False)
    crew = db.Column(db.Integer, unique=False, nullable=False)
    passengers = db.Column(db.Integer, unique=False, nullable=False)
    favorite_vehicle = db.relationship('FavoriteVehicle', backref = 'vehicle', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers
            # do not serialize the password, its a security breach
        }

class FavoriteVehicle(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicle": Vehicle.query.get(self.vehicle_id).serialize()
        }

#recomendacion separar los favoritos en tablas distintas
# new_favorite = FavoritePeople(user_id = db.Column....., )
# new_favorite.user -> obtengo toda la info del usuario q tiene a ese favorito en su lista y tmb obtengo sus metodos (serialize)

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)
    rotation_period = db.Column(db.Integer, unique=False, nullable=False)
    orbital_period = db.Column(db.Integer, unique=False, nullable=False)
    gravity = db.Column(db.Integer, unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    climate = db.Column(db.String(50), unique=False, nullable=False)
    terrain = db.Column(db.String(50), unique=False, nullable=False)
    surface_water = db.Column(db.String(50), unique=False, nullable=False)
    favorite_planet = db.relationship('FavoritePlanet', backref = 'planet', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water
            # do not serialize the password, its a security breach
        }

class FavoritePlanet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user": User.query.get(self.user_id).serialize(),
            "planet": Planet.query.get(self.planet_id).serialize()
        }