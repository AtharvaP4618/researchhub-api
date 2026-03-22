from app.extensions import db, bcrypt
import string
from datetime import datetime, UTC

class Resource(db.Model):
    __tablename__ = "resources"


    id = db.Column(db.Integer, primary_key=True)
