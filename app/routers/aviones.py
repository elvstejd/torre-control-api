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


@router.get('/aviones/', tags=['aviones'])
def listar_aviones(db: Session = Depends(get_db)):
    aviones = db.query(Avion).all()
    return aviones
