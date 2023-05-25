from fastapi import APIRouter
from schemas import PasajeroRequest, PasajeroResponse, MessageResponse
from sqlalchemy.orm import Session
from models import Pasajero
from db import get_db
from fastapi import Depends

router = APIRouter()


@router.post('/pasajeros/', tags=['pasajeros'], response_model=PasajeroResponse)
def registrar_pasajero(pasajero: PasajeroRequest, db: Session = Depends(get_db)):
    pasajero = Pasajero(**pasajero.dict())

    db.add(pasajero)
    db.commit()
    db.refresh(pasajero)

    return pasajero


@router.delete('/pasajeros/{pasajero_id}', tags=['pasajeros'], response_model=MessageResponse)
def eliminar_pasajero(pasajero_id: int, db: Session = Depends(get_db)):
    pasajero = db.query(Pasajero).filter(Pasajero.id == pasajero_id).first()
    db.delete(pasajero)
    db.commit()
    return MessageResponse(message='Pasajero eliminado')
