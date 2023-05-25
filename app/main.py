from routers import aviones, pasajeros, aeropuertos
from db import engine
from fastapi import FastAPI
import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(aviones.router)
app.include_router(pasajeros.router)


@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Torre de Control"}
