from __main__ import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)


class Tarea(db.Model):
    __tablename__ = 'tarea'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable = False)
    completada = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, nullable = False)
    fecha_finalizacion = db.Column(db.DateTime, nullable=True)
    
    