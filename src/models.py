from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    fav_planets = db.relationship('FavPlanets', lazy=True)
    fav_characters = db.relationship('FavCharacters', lazy=True)


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            # "planets": list(map(lambda x: x.serialize, self.fav_planets)),
            # "characters": list(map(lambda x: x.serialize, self.fav_characters))
            # do not serialize the password, its a security breach
        }
    def favorites(self):
        return {
            "planets": self.fav_planets,
            "characters": self.fav_characters,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Personaje(db.Model):
    __tablename__ = 'personajes'
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Integer, unique=False, nullable=False)
    mass = db.Column(db.Integer, unique=False, nullable=False)
    hair_color = db.Column(db.String(80), unique=False, nullable=False)
    skin_color = db.Column(db.String(50), unique=False, nullable=False)
    eye_color = db.Column(db.String(50), unique=False, nullable=False)
    birth_year = db.Column(db.String(50), unique=False, nullable=False)
    gender = db.Column(db.String(50), unique=False, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    url = db.Column(db.String(50), unique=False, nullable=False)
    tipo = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return '<Personaje %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "name": self.name,
            "url": self.url,
            "tipo": self.tipo
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    diameter = db.Column(db.Integer, unique=False, nullable=False)
    population = db.Column(db.String(80), unique=False, nullable=False)
    surface_water = db.Column(db.Integer, unique=False, nullable=False)
    gravity = db.Column(db.String(80), unique=False, nullable=False)
    climate = db.Column(db.String(50), unique=False, nullable=False)
    terrain = db.Column(db.String(50), unique=False, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    url = db.Column(db.String(50), unique=False, nullable=False)
    tipo = db.Column(db.String(50), unique=False, nullable=False)
    def __repr__(self):
        return '<Planeta %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "diameter": self.diameter,
            "population": self.population,
            "surface_water": self.surface_water,
            "gravity": self.gravity,
            "climate": self.climate,
            "terrain": self.terrain,
            "name": self.name,
            "url": self.url,
            "tipo": self.tipo

            # do not serialize the password, its a security breach
        }

class FavPlanets(db.Model):
    __tablename__ = 'favplanets'
    id = db.Column(db.Integer, primary_key=True)
    planetId = db.Column(db.Integer, db.ForeignKey('planets.id'))
    typeOfFav = db.Column(db.String(50), unique=False, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(50), unique=False, nullable=False)
    
    def __repr__(self):
        return '<FavPlanets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "planetId": self.planetId,
            "name": self.name
            # do not serialize the password, its a security breach
        }
        
class FavCharacters(db.Model):
    __tablename__ = 'favcharacters'
    id = db.Column(db.Integer, primary_key=True)
    typeOfFav = db.Column(db.String(50), unique=False, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    characterId = db.Column(db.Integer, db.ForeignKey('personajes.id'))
    name = db.Column(db.String(50), unique=False, nullable=False)
    def __repr__(self):
        return '<FavCharacters %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "characterId": self.characterId,
            "name": self.name
            # do not serialize the password, its a security breach
        }


# class FavCharacters(Base):
#     __tablename__ = 'favCharacters'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     userId = Column(Integer, ForeignKey('user.id'))
#     characterId = Column(Integer, ForeignKey('character.id'))
    


#     def to_dict(self):
#         return {}

# ## Draw from SQLAlchemy base
# render_er(Base, 'diagram.png')