""" Interfaces para los repositorios del dominio de cliente

En este archivo usted encontrará las diferentes interfaces para los repositorios
del dominio de cliente

"""

from abc import ABC
from aeroalpes.seedwork.dominio.repositorios import Repositorio

class RepositorioUsuarios(Repositorio, ABC):
    ...
