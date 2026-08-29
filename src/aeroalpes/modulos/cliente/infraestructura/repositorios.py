from aeroalpes.config.db import db
from aeroalpes.modulos.cliente.dominio.entidades import Usuario
from aeroalpes.modulos.cliente.dominio.repositorios import RepositorioUsuarios
from .dto import Usuario as UsuarioDTO
from .mapeadores import MapeadorUsuario
from uuid import UUID


class RepositorioUsuariosSQLite(RepositorioUsuarios):

    def __init__(self):
        self._mapeador = MapeadorUsuario()

    def obtener_por_id(self, id: UUID) -> Usuario:
        usuario_dto = db.session.query(UsuarioDTO).filter_by(id=str(id)).one()
        return self._mapeador.dto_a_entidad(usuario_dto)

    def obtener_todos(self) -> list[Usuario]:
        return [self._mapeador.dto_a_entidad(dto) for dto in db.session.query(UsuarioDTO).all()]

    def agregar(self, usuario: Usuario):
        usuario_dto = self._mapeador.entidad_a_dto(usuario)
        db.session.add(usuario_dto)

    def actualizar(self, usuario: Usuario):
        raise NotImplementedError

    def eliminar(self, usuario_id: UUID):
        raise NotImplementedError
