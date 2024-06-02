from .extensions import db 
import uuid

class PKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strain = db.Column(db.String(50))
    uuid = db.Column(db.String(50))