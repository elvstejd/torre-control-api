from fastapi import APIRouter
from schemas import AterrizajeRequest, AterrizajeResponse
from sqlalchemy.orm import Session
from models import Aeropuerto, Vuelo, Aterrizaje
from db import get_db
from fastapi import Depends

router = APIRouter()


@router.post('/aterrizajes/', tags=['aterrizajes'], response_model=AterrizajeResponse)
def registrar_aterrizaje(aterrizaje: AterrizajeRequest, db: Session = Depends(get_db)):
    aterrizaje = Aterrizaje(**aterrizaje.dict())
    vuelo = db.query(Vuelo).filter(Vuelo.id == aterrizaje.vuelo_id).first()

    vuelo.estado = 'finalizado'
    db.add(vuelo)

    db.add(aterrizaje)
    db.commit()
    db.refresh(vuelo)
    db.refresh(aterrizaje)

    return aterrizaje


@router.get('/aterrizajes/', tags=['aterrizajes'], response_model=list[AterrizajeResponse])
def listar_aterrizajes(db: Session = Depends(get_db)):
    aterrizajes = db.query(Aterrizaje).all()

    return aterrizajes
