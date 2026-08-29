from dataclasses import dataclass
from aeroalpes.seedwork.dominio.fabricas import Fabrica
from aeroalpes.seedwork.dominio.repositorios import Repositorio
from aeroalpes.modulos.cliente.dominio.repositorios import RepositorioUsuarios
from .repositorios import RepositorioUsuariosSQLite


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioUsuarios.__class__:
            return RepositorioUsuariosSQLite()
        raise Exception(f'No existe fábrica para el repositorio {obj}')
