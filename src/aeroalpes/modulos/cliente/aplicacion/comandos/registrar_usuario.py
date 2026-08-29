from dataclasses import dataclass
from aeroalpes.seedwork.aplicacion.comandos import Comando, ComandoHandler
from aeroalpes.seedwork.aplicacion.comandos import ejecutar_commando as comando
from aeroalpes.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from aeroalpes.modulos.cliente.dominio.entidades import Usuario
from aeroalpes.modulos.cliente.dominio.objetos_valor import Email, Nombre
from aeroalpes.modulos.cliente.dominio.repositorios import RepositorioUsuarios
from aeroalpes.modulos.cliente.infraestructura.fabricas import FabricaRepositorio


def _partir_email(email: str):
    if email and '@' in email:
        address, dominio = email.rsplit('@', 1)
        return address, dominio
    return email or '', ''


@dataclass
class RegistrarUsuario(Comando):
    nombres: str
    apellidos: str
    email: str
    password: str
    es_empresarial: bool


class RegistrarUsuarioHandler(ComandoHandler):

    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()

    def handle(self, comando: RegistrarUsuario):
        address, dominio = _partir_email(comando.email)
        usuario = Usuario(
            nombre=Nombre(nombres=comando.nombres, apellidos=comando.apellidos),
            email=Email(address=address, dominio=dominio, es_empresarial=comando.es_empresarial),
        )
        usuario.registrar_usuario(usuario)

        repositorio = self._fabrica_repositorio.crear_objeto(RepositorioUsuarios.__class__)
        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, usuario)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(RegistrarUsuario)
def ejecutar_comando_registrar_usuario(comando: RegistrarUsuario):
    handler = RegistrarUsuarioHandler()
    handler.handle(comando)
