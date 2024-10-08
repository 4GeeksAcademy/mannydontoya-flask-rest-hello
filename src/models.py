from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.user_name

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=True)
    eye_color = db.Column(db.String(250), nullable=True)
    hair_color = db.Column(db.String(250), nullable=True)
    height = db.Column(db.String(250), nullable=True)
    skin_color = db.Column(db.String(250), nullable=True)
    mass = db.Column(db.String(250), nullable=True)
    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "height": self.height,
            "skin_color": self.skin_color,
            "mass": self.mass
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=True)
    population = db.Column(db.String(250), nullable=True)
    gravity = db.Column(db.String(250), nullable=True)
    rotation_period = db.Column(db.String(250), nullable=True)
    terrain = db.Column(db.String(250), nullable=True)
    mass = db.Column(db.String(250), nullable=True)
    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "user_id" : self.user_id,
            "name": self.name,
            "climate" : self.climate,
            "population" : self.population,
            "gravity" : self.gravity,
            "rotation_period" : self.rotation_period,
            "terrain" : self.terrain,
            "mass" : self.mass,
        }




class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
    character_id = db.Column(db.Integer, db.ForeignKey(Character.id))
    character = db.relationship(Character)
    planet_id = db.Column(db.Integer, db.ForeignKey(Planet.id))
    planet = db.relationship(Planet)
    def __repr__(self):
        return '<Favorite %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "user": self.user,
            "character": self.character,
            "planet": self.planet
        }


