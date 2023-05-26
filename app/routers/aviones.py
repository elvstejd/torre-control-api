import os
import sys
from fastapi import APIRouter
from schemas import AvionRequest, AvionResponse, MessageResponse, AvionDetalleResponse
from sqlalchemy.orm import Session
from models import Avion, Vuelo
from db import get_db
from fastapi import Depends

router = APIRouter()


if '__file__' in vars():
    path = os.path.join(os.path.dirname(__file__), os.pardir)
    sys.path.append(path)
else:
    sys.path.append(os.pardir)


from utils import model_to_dict   # noqa: E402


@router.post('/aviones/', tags=['aviones'], response_model=AvionResponse)
def registrar_avion(avion: AvionRequest, db: Session = Depends(get_db)):
    avion = Avion(**avion.dict())

    db.add(avion)
    db.commit()
    db.refresh(avion)

    return avion


@router.get('/aviones/{avion_id}', tags=['aviones'], response_model=AvionDetalleResponse)
def obtener_avion(avion_id: int, db: Session = Depends(get_db)):
    avion = db.query(Avion).filter(Avion.id == avion_id).first()
    vuelos = db.query(Vuelo).filter(Vuelo.avion_id == avion_id).all()

    return {
        **model_to_dict(avion),
        'vuelos': [model_to_dict(vuelo) for vuelo in vuelos]
    }


@router.get('/aviones/', tags=['aviones'], response_model=list[AvionResponse])
def listar_aviones(db: Session = Depends(get_db)):
    aviones = db.query(Avion).all()
    return aviones


@router.delete('/aviones/{avion_id}', tags=['aviones'], response_model=MessageResponse)
def eliminar_avion(avion_id: int, db: Session = Depends(get_db)):
    avion = db.query(Avion).filter(Avion.id == avion_id).first()
    db.delete(avion)
    db.commit()
    return MessageResponse(message='Avion eliminado')
