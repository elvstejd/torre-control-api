from routers import aviones, pasajeros, aeropuertos
from db import engine
from fastapi import FastAPI
import models
import uvicorn

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(aviones.router)
app.include_router(pasajeros.router)
app.include_router(aeropuertos.router)


@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Torre de Control"}


# run app with uvicorn in reload mode
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3002, reload=True)
