from pydantic import BaseModel
from datetime import datetime


class OrmModeBaseModel(BaseModel):
    class Config:
        orm_mode = True


class AvionRequest(BaseModel):
    nombre: str
    limite_pasajeros: int
    limite_peso_kg: int
    aeropuerto_actual_id: int


class AvionResponse(OrmModeBaseModel):
    id: int
    nombre: str
    limite_pasajeros: int
    limite_peso_kg: int
    aeropuerto_actual_id: int


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
        super().__init__(message=message)


class VueloRequest(BaseModel):
    avion_id: int
    aeropuerto_origen_id: int
    aeropuerto_destino_id: int
    fecha_salida: str
    fecha_llegada: str


class VueloResponse(OrmModeBaseModel):
    id: int
    avion_id: int
    aeropuerto_origen_id: int
    aeropuerto_destino_id: int
    fecha_salida: datetime
    fecha_llegada: datetime
    estado: str
    duracion: str


class VueloResumen(OrmModeBaseModel):
    id: int
    aeropuerto_origen_id: int
    aeropuerto_destino_id: int
    fecha_salida: datetime
    fecha_llegada: datetime
    estado: str


class AvionDetalleResponse(AvionResponse):
    vuelos: list[VueloResumen]


class PasajeroVueloRequest(BaseModel):
    pasajero_id: int
    peso_equipaje: int


class PasajeroVueloResponse(OrmModeBaseModel):
    vuelo_id: int
    total_pasajeros: int
    limite_pasajeros: int
    total_peso_equipaje: int
    limite_peso_equipaje: int
    pasajeros: list[PasajeroResponse]


class DespegueRequest(BaseModel):
    vuelo_id: int
    aeropuerto_id: int


class DespegueResponse(OrmModeBaseModel):
    id: int
    vuelo_id: int
    aeropuerto_id: int
    hora: datetime


class AterrizajeRequest(BaseModel):
    vuelo_id: int
    aeropuerto_id: int


class AterrizajeResponse(OrmModeBaseModel):
    id: int
    vuelo_id: int
    aeropuerto_id: int
    hora: datetime
