from functools import singledispatch

import pulsar
from pulsar.schema import *

from aeroalpes.modulos.vuelos.aplicacion.comandos.crear_reserva import CrearReserva
from aeroalpes.modulos.vuelos.infraestructura.schema.v1.eventos import EventoReservaCreada, ReservaCreadaPayload
from aeroalpes.modulos.vuelos.infraestructura.schema.v1.comandos import (
    ComandoCrearReserva,
    ComandoCrearReservaPayload,
    Itinerario,
    Leg,
    Locacion,
    Odo,
    Segmento,
)
from aeroalpes.seedwork.infraestructura import utils

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


def itinerarios_a_avro(itinerarios):
    records = []
    for itinerario in itinerarios or []:
        odos = []
        for odo in itinerario.odos:
            segmentos = []
            for segmento in odo.segmentos:
                legs = []
                for leg in segmento.legs:
                    origen = locacion_a_avro(leg.origen)
                    destino = locacion_a_avro(leg.destino)
                    legs.append(Leg(
                        fecha_salida=leg.fecha_salida,
                        fecha_llegada=leg.fecha_llegada,
                        origen=origen,
                        destino=destino,
                    ))
                segmentos.append(Segmento(legs=legs))
            odos.append(Odo(segmentos=segmentos))
        records.append(Itinerario(odos=odos))
    return records


def locacion_a_avro(locacion):
    if isinstance(locacion, dict):
        return Locacion(codigo=locacion.get('codigo'), nombre=locacion.get('nombre'))
    return Locacion(codigo=getattr(locacion, 'codigo', None), nombre=getattr(locacion, 'nombre', None))


@singledispatch
def comando_a_integracion(comando):
    raise NotImplementedError(f'No existe implementación para el comando de tipo {type(comando).__name__}')


@comando_a_integracion.register(CrearReserva)
def _(comando: CrearReserva):
    payload = ComandoCrearReservaPayload(
        id_usuario=comando.id_usuario,
        itinerarios=itinerarios_a_avro(comando.itinerarios)
    )
    return ComandoCrearReserva(data=payload)


class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        payload = ReservaCreadaPayload(
            id_reserva=str(evento.id_reserva), 
            id_cliente=str(evento.id_cliente), 
            estado=str(evento.estado), 
            fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
        )
        evento_integracion = EventoReservaCreada(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoReservaCreada))

    def publicar_comando(self, comando, topico):
        comando_integracion = comando_a_integracion(comando)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(type(comando_integracion)))
