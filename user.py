from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password