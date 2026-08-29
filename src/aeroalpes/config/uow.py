from aeroalpes.config.db import db
from aeroalpes.seedwork.dominio.entidades import AgregacionRaiz
from aeroalpes.seedwork.infraestructura.uow import Batch, Lock, UnidadTrabajo

class UnidadTrabajoSQLAlchemy(UnidadTrabajo):

    def __init__(self):
        self._batches: list[Batch] = list()

    def __enter__(self) -> UnidadTrabajo:
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()

    def _limpiar_batches(self):
        self._batches = list()

    @property
    def savepoints(self) -> list:
        return list[db.session.get_nested_transaction()]

    @property
    def batches(self) -> list[Batch]:
        return self._batches             

    def _aplicar_lock(self, batch: Batch):
        if batch.lock != Lock.PESIMISTA:
            return

        for arg in batch.args:
            if not isinstance(arg, AgregacionRaiz) or not getattr(arg, 'id', None):
                continue
            id_agregado = str(arg.id)
            for persistido in db.session.identity_map.values():
                if str(getattr(persistido, 'id', '')) != id_agregado:
                    continue
                db.session.refresh(persistido, with_for_update=True)

    def commit(self):
        for batch in self.batches:
            self._aplicar_lock(batch)
            batch.operacion(*batch.args, **batch.kwargs)

        db.session.commit()

        super().commit()

    def rollback(self, savepoint=None):
        if savepoint:
            savepoint.rollback()
        else:
            db.session.rollback()
        
        super().rollback()
    
    def savepoint(self):
        db.session.begin_nested()