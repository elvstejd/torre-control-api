from fastapi import APIRouter, HTTPException
from schemas import VueloRequest, VueloResponse, MessageResponse, PasajeroVueloRequest, PasajeroVueloResponse
from sqlalchemy.orm import Session
from models import Vuelo, PasajeroVuelo, Avion, Pasajero
from db import get_db
from fastapi import Depends
from sqlalchemy.sql import func
from sqlalchemy import text, select


import sys
import os

if '__file__' in vars():
    path = os.path.join(os.path.dirname(__file__), os.pardir)
    sys.path.append(path)
else:
    sys.path.append(os.pardir)


from app.utils import model_to_dict, calcular_duracion   # noqa: E402


router = APIRouter()


@router.post('/vuelos/', tags=['vuelos'], response_model=VueloResponse)
def registrar_vuelo(vuelo: VueloRequest, db: Session = Depends(get_db)):
    vuelo = Vuelo(**vuelo.dict())
    duracion = calcular_duracion(vuelo.fecha_salida, vuelo.fecha_llegada)

    db.add(vuelo)
    db.commit()
    db.refresh(vuelo)

    return {
        **model_to_dict(vuelo),
        'duracion': str(duracion) + ' horas'
    }


@router.get('/vuelos/{vuelo_id}', tags=['vuelos'], response_model=VueloResponse)
def obtener_vuelo(vuelo_id: int, db: Session = Depends(get_db)):
    vuelo = db.query(Vuelo).filter(Vuelo.id == vuelo_id).first()
    duracion = calcular_duracion(vuelo.fecha_salida, vuelo.fecha_llegada)

    return {
        **model_to_dict(vuelo),
        'duracion': str(duracion) + ' horas'
    }


@router.get('/vuelos/', tags=['vuelos'], response_model=list[VueloResponse])
def listar_vuelos(db: Session = Depends(get_db)):
    vuelos = db.query(Vuelo).all()

    return [
        {
            **model_to_dict(vuelo),
            'duracion': str(calcular_duracion(vuelo.fecha_salida, vuelo.fecha_llegada)) + ' horas'
        } for vuelo in vuelos
    ]


@router.delete('/vuelos/{vuelo_id}', tags=['vuelos'], response_model=MessageResponse)
def eliminar_vuelo(vuelo_id: int, db: Session = Depends(get_db)):
    vuelo = db.query(Vuelo).filter(
        Vuelo.id == vuelo_id).first()
    db.delete(vuelo)
    db.commit()

    return MessageResponse(message='Vuelo eliminado')


@router.post('/vuelos/{vuelo_id}/pasajeros/', tags=['vuelos'], responses={200: {"model": PasajeroVueloResponse}, 400: {"class": HTTPException}})
def agregar_pasajero_a_vuelo(pasajero: PasajeroVueloRequest, vuelo_id: int, db: Session = Depends(get_db)):
    vuelo = db.query(Vuelo).filter(Vuelo.id == vuelo_id).first()
    avion = db.query(Avion).filter(Avion.id == vuelo.avion_id).first()
    limite_pasajeros = avion.limite_pasajeros
    limite_equipaje = avion.limite_peso_kg

    pasajeros_a_bordo = db.query(PasajeroVuelo).filter(
        PasajeroVuelo.vuelo_id == vuelo_id).count()

    peso_actual_equipaje = db.query(
        func.sum(PasajeroVuelo.peso_equipaje)).filter(PasajeroVuelo.vuelo_id == vuelo_id).scalar(
    )

    if pasajeros_a_bordo >= limite_pasajeros:
        return HTTPException(status_code=400, detail='No hay cupo en el vuelo')

    if peso_actual_equipaje + pasajero.peso_equipaje > limite_equipaje:
        return HTTPException(status_code=400, detail='No hay espacio para el equipaje del pasajero. Necesita reducir ' + str(abs(limite_equipaje - peso_actual_equipaje - pasajero.peso_equipaje)) + ' kg.')

    pasajero_en_vuelo = PasajeroVuelo(
        vuelo_id=vuelo_id,
        pasajero_id=pasajero.pasajero_id,
        peso_equipaje=pasajero.peso_equipaje
    )

    db.add(pasajero_en_vuelo)
    db.commit()

    return MessageResponse(message='Pasajero agregado al vuelo')


@router.get('/vuelos/{vuelo_id}/pasajeros/', tags=['vuelos'], response_model=PasajeroVueloResponse)
def listar_pasajeros_de_vuelo(vuelo_id: int, db: Session = Depends(get_db)):
    vuelo = db.query(Vuelo).filter(Vuelo.id == vuelo_id).first()
    registro_pasajeros_vuelo = db.query(PasajeroVuelo).filter(
        PasajeroVuelo.vuelo_id == vuelo_id).all()
    avion = db.query(Avion).filter(Avion.id == vuelo.avion_id).first()

    pasajeros = []
    for registro in registro_pasajeros_vuelo:
        pasajero = db.query(Pasajero).filter(
            Pasajero.id == registro.pasajero_id).first()
        pasajeros.append(model_to_dict(pasajero))

    return {
        'vuelo_id': vuelo_id,
        'total_pasajeros': len(pasajeros),
        'limite_pasajeros': avion.limite_pasajeros,
        'total_peso_equipaje': sum([registro.peso_equipaje for registro in registro_pasajeros_vuelo]),
        'limite_peso_equipaje': avion.limite_peso_kg,
        'pasajeros': pasajeros
    }
