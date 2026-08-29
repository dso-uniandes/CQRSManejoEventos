from dataclasses import dataclass
from aeroalpes.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from aeroalpes.seedwork.aplicacion.queries import ejecutar_query as query
from aeroalpes.modulos.cliente.dominio.repositorios import RepositorioUsuarios
from aeroalpes.modulos.cliente.infraestructura.fabricas import FabricaRepositorio


def _partir_email(email: str):
    if email and '@' in email:
        address, dominio = email.rsplit('@', 1)
        return address, dominio
    return email or '', ''


@dataclass
class ObtenerUsuario(Query):
    id: str = None
    email: str = None


class ObtenerUsuarioHandler(QueryHandler):

    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()

    def handle(self, query: ObtenerUsuario) -> QueryResultado:
        repositorio = self._fabrica_repositorio.crear_objeto(RepositorioUsuarios.__class__)
        if query.id:
            usuario = repositorio.obtener_por_id(query.id)
        else:
            address, dominio = _partir_email(query.email)
            usuario = repositorio.obtener_por_email(address, dominio)
        return QueryResultado(resultado=usuario)


@query.register(ObtenerUsuario)
def ejecutar_query_obtener_usuario(query: ObtenerUsuario):
    handler = ObtenerUsuarioHandler()
    return handler.handle(query)
