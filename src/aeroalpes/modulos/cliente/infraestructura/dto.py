"""DTOs para la capa de infrastructura del dominio de clientes

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio del cliente

"""

from aeroalpes.config.db import db


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.String, primary_key=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    nombres = db.Column(db.String)
    apellidos = db.Column(db.String)
    email_address = db.Column(db.String)
    email_dominio = db.Column(db.String)
    es_empresarial = db.Column(db.Boolean)
