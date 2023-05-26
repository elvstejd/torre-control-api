from pydantic import BaseModel
from datetime import datetime


class OrmModeBaseModel(BaseModel):
    class Config:
        orm_mode = True


class AvionRequest(BaseModel):
    nombre: str
    limite_pasajeros: int
    limite_peso_kg: int


class AvionResponse(OrmModeBaseModel):
    id: int
    nombre: str
    limite_pasajeros: int
    limite_peso_kg: int


class PasajeroRequest(BaseModel):
    nombre: str


class PasajeroResponse(OrmModeBaseModel):
    id: int
    nombre: str


class AeropuertoRequest(BaseModel):
    nombre: str
    limite_aviones: int


class AeropuertoResponse(OrmModeBaseModel):
    id: int
    nombre: str
    limite_aviones: int


class MessageResponse(BaseModel):
    message: str

    def __init__(self, message: str):
        self.message = message


