import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback

from aeroalpes.modulos.vuelos.aplicacion.comandos.crear_reserva import CrearReserva
from aeroalpes.modulos.vuelos.aplicacion.dto import ItinerarioDTO, LegDTO, OdoDTO, SegmentoDTO
from aeroalpes.modulos.vuelos.infraestructura.schema.v1.eventos import EventoReservaCreada
from aeroalpes.modulos.vuelos.infraestructura.schema.v1.comandos import ComandoCrearReserva
from aeroalpes.seedwork.aplicacion.comandos import ejecutar_commando
from aeroalpes.seedwork.infraestructura import utils


def locacion_a_dict(locacion):
    if locacion is None:
        return dict()
    return dict(codigo=getattr(locacion, 'codigo', None), nombre=getattr(locacion, 'nombre', None))


def itinerarios_avro_a_dto(itinerarios):
    itinerarios_dto = list()
    for itinerario in itinerarios or []:
        odos_dto = list()
        for odo in itinerario.odos or []:
            segmentos_dto = list()
            for segmento in odo.segmentos or []:
                legs_dto = list()
                for leg in segmento.legs or []:
                    legs_dto.append(LegDTO(
                        fecha_salida=leg.fecha_salida,
                        fecha_llegada=leg.fecha_llegada,
                        origen=locacion_a_dict(leg.origen),
                        destino=locacion_a_dict(leg.destino),
                    ))
                segmentos_dto.append(SegmentoDTO(legs_dto))
            odos_dto.append(OdoDTO(segmentos_dto))
        itinerarios_dto.append(ItinerarioDTO(odos_dto))
    return itinerarios_dto


def comando_integracion_a_comando_aplicacion(comando_integracion: ComandoCrearReserva) -> CrearReserva:
    payload = comando_integracion.data
    return CrearReserva(
        fecha_creacion='',
        fecha_actualizacion='',
        id='',
        id_usuario=payload.id_usuario,
        itinerarios=itinerarios_avro_a_dto(payload.itinerarios),
    )

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-reserva', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='aeroalpes-sub-eventos', schema=AvroSchema(EventoReservaCreada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-reserva', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='aeroalpes-sub-comandos', schema=AvroSchema(ComandoCrearReserva))

        while True:
            mensaje = consumidor.receive()
            comando_integracion = mensaje.value()
            comando = comando_integracion_a_comando_aplicacion(comando_integracion)
            ejecutar_commando(comando)
            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()