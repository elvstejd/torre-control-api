from pydantic import BaseModel


class AvionRequest(BaseModel):
    nombre: str
    limite_pasajeros: int
    limite_peso_kg: int


