from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes import create_app


app = create_app()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prerate.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Definizione del modello del database
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    tokens = db.Column(db.Integer, nullable=False)
    api_key = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "tokens": self.tokens,
            "api_key": self.api_key,
            "password": self.password,
        }


# Creazione del database (eseguire una sola volta)
# @app.before_first_request
# def create_tables():
#     db.create_all()
