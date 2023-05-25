from fastapi import APIRouter
from schemas import AvionRequest
from sqlalchemy.orm import Session
from models import Avion
from db import get_db
from fastapi import Depends

router = APIRouter()


@router.post('/aviones/', tags=['aviones'])
def registrar_avion(avion: AvionRequest, db: Session = Depends(get_db)):
    avion = Avion(**avion.dict())

    db.add(avion)
    db.commit()
    db.refresh(avion)

    return avion


@router.get('/aviones/{avion_id}', tags=['aviones'])
def obtener_avion(avion_id: int, db: Session = Depends(get_db)):
    avion = db.query(Avion).filter(Avion.id == avion_id).first()
    return avion


@router.get('/aviones/', tags=['aviones'])
def listar_aviones(db: Session = Depends(get_db)):
    aviones = db.query(Avion).all()
    return aviones


@router.delete('/aviones/{avion_id}', tags=['aviones'])
def eliminar_avion(avion_id: int, db: Session = Depends(get_db)):
    avion = db.query(Avion).filter(Avion.id == avion_id).first()
    db.delete(avion)
    db.commit()
    return {'message': 'Avion eliminado'}
