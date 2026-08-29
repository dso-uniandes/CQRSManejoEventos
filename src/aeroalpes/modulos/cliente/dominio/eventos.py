from __future__ import annotations
from dataclasses import dataclass
from aeroalpes.seedwork.dominio.eventos import EventoDominio
import uuid


@dataclass
class UsuarioRegistrado(EventoDominio):
    id_usuario: uuid.UUID = None


@dataclass
class UsuarioValidado(EventoDominio):
    id_usuario: uuid.UUID = None
