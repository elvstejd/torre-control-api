from fastapi import APIRouter
from schemas import AeropuertoRequest, AeropuertoResponse, MessageResponse
from sqlalchemy.orm import Session
from models import Aeropuerto
from db import get_db
from fastapi import Depends

router = APIRouter()


@router.post('/aeropuertos/', tags=['aeropuertos'], response_model=AeropuertoResponse)
def registrar_aeropuerto(aeropuerto: AeropuertoRequest, db: Session = Depends(get_db)):
    aeropuerto = Aeropuerto(**aeropuerto.dict())

    db.add(aeropuerto)
    db.commit()
    db.refresh(aeropuerto)

    return aeropuerto


@router.get('/aeropuertos/', tags=['aeropuertos'], response_model=list[AeropuertoResponse])
def listar_aeropuertos(db: Session = Depends(get_db)):

    aeropuertos = db.query(Aeropuerto).all()

    return aeropuertos


@router.delete('/aeropuertos/{aeropuerto_id}', tags=['aeropuertos'], response_model=MessageResponse)
def eliminar_aeropuerto(aeropuerto_id: int, db: Session = Depends(get_db)):
    aeropuerto = db.query(Aeropuerto).filter(
        Aeropuerto.id == aeropuerto_id).first()
    db.delete(aeropuerto)
    db.commit()
    return MessageResponse(message='Aeropuerto eliminado')
