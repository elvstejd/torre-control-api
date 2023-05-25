from pydantic import BaseModel


class AvionRequest(BaseModel):
    nombre: str
    limite_pasajeros: int
    limite_peso_kg: int


class AvionResponse(BaseModel):
    id: int
    nombre: str
    limite_pasajeros: int
    limite_peso_kg: int


class PasajeroRequest(BaseModel):
    nombre: str


class PasajeroResponse(BaseModel):
    id: int
    nombre: str



class MessageResponse(BaseModel):
    message: str

    def __init__(self, message: str):
        self.message = message


