from aeroalpes.seedwork.dominio.repositorios import Mapeador
from aeroalpes.modulos.cliente.dominio.entidades import Usuario
from aeroalpes.modulos.cliente.dominio.objetos_valor import Email, Nombre
from .dto import Usuario as UsuarioDTO


class MapeadorUsuario(Mapeador):

    def obtener_tipo(self) -> type:
        return Usuario.__class__

    def entidad_a_dto(self, entidad: Usuario) -> UsuarioDTO:
        usuario_dto = UsuarioDTO()
        usuario_dto.id = str(entidad.id)
        usuario_dto.fecha_creacion = entidad.fecha_creacion
        usuario_dto.fecha_actualizacion = entidad.fecha_actualizacion
        usuario_dto.nombres = entidad.nombre.nombres
        usuario_dto.apellidos = entidad.nombre.apellidos
        usuario_dto.email_address = entidad.email.address
        usuario_dto.email_dominio = entidad.email.dominio
        usuario_dto.es_empresarial = entidad.email.es_empresarial
        return usuario_dto

    def dto_a_entidad(self, dto: UsuarioDTO) -> Usuario:
        usuario = Usuario()
        usuario.nombre = Nombre(nombres=dto.nombres, apellidos=dto.apellidos)
        usuario.email = Email(
            address=dto.email_address,
            dominio=dto.email_dominio,
            es_empresarial=dto.es_empresarial,
        )
        return usuario
