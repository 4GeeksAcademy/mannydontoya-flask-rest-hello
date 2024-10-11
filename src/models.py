from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorite_planets = db.Table(
    "favorite_planets",
    db.Column("user_id", db.ForeignKey("user.id")),
    db.Column("planet_id", db.ForeignKey("planet.id")),
)    

favorite_characters = db.Table(
    "favorite_characters",
    db.Column("user_id", db.ForeignKey("user.id")),
    db.Column("character_id", db.ForeignKey("character.id")),
)  

class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    favorite_planets = db.relationship("Planet", secondary=favorite_planets)
    favorite_characters = db.relationship("Character", secondary=favorite_characters)
    def __repr__(self):
        return '<User %r>' % self.user_name

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "favorite_planets": [planet.serialize() for planet in self.favorite_planets],
            "favorite_characters": [character.serialize() for character in self.favorite_characters]
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    __tablename__="character"
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
    __tablename__="planet"
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
            "name": self.name,
            "climate" : self.climate,
            "population" : self.population,
            "gravity" : self.gravity,
            "rotation_period" : self.rotation_period,
            "terrain" : self.terrain,
            "mass" : self.mass,
        }




 


