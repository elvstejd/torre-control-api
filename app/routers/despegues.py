from fastapi import APIRouter
from schemas import DespegueRequest, DespegueResponse
from sqlalchemy.orm import Session
from models import Aeropuerto, Vuelo, Despegue
from db import get_db
from fastapi import Depends

router = APIRouter()


@router.post('/despegues/', tags=['despegues'], response_model=DespegueResponse)
def registrar_despegue(despegue: DespegueRequest, db: Session = Depends(get_db)):
    despegue = Despegue(**despegue.dict())
    vuelo = db.query(Vuelo).filter(Vuelo.id == despegue.vuelo_id).first()

    vuelo.estado = 'en_proceso'
    db.add(vuelo)

    db.add(despegue)
    db.commit()
    db.refresh(vuelo)
    db.refresh(despegue)

    return despegue


@router.get('/despegues/', tags=['despegues'], response_model=list[DespegueResponse])
def listar_despegues(db: Session = Depends(get_db)):
    despegues = db.query(Despegue).all()

    return despegues
