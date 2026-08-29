"""Entidades del dominio de cliente

En este archivo usted encontrará las entidades del dominio de cliente

"""

from datetime import datetime
from aeroalpes.seedwork.dominio.entidades import AgregacionRaiz
from dataclasses import dataclass, field

from .eventos import UsuarioRegistrado
from .objetos_valor import Nombre, Email, Cedula, Rut

@dataclass
class Usuario(AgregacionRaiz):
    nombre: Nombre = field(default_factory=Nombre)
    email: Email = field(default_factory=Email)

    def registrar_usuario(self, usuario: 'Usuario'):
        self.nombre = usuario.nombre
        self.email = usuario.email
        self.agregar_evento(UsuarioRegistrado(id_usuario=self.id))

@dataclass
class ClienteNatural(Usuario):
    cedula: Cedula = field(default_factory=Cedula)
    fecha_nacimiento: datetime = field(default_factory=datetime)

@dataclass
class ClienteEmpresa(Usuario):
    rut: Rut = field(default_factory=Rut)
    fecha_constitucion: datetime = field(default_factory=datetime)
