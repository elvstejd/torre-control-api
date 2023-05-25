from db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum


class Avion(Base):
    __tablename__ = "aviones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    limite_pasajeros = Column(Integer)
    limite_peso_kg = Column(Integer)


class Aeropuerto(Base):
    __tablename__ = "aeropuertos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    limite_aviones = Column(Integer)


class Vuelo(Base):
    __tablename__ = "vuelos"

    id = Column(Integer, primary_key=True, index=True)
    avion_id = Column(Integer, ForeignKey("aviones.id"))
    aeropuerto_origen_id = Column(Integer, ForeignKey("aeropuertos.id"))
    aeropuerto_destino_id = Column(Integer, ForeignKey("aeropuertos.id"))
    fecha_salida = Column(DateTime)
    fecha_llegada = Column(DateTime)
    estado = Column(Enum("programado", "en_proceso", "finalizado",
                    name="estado_vuelo"), default="programado")


class Pasajero(Base):
    __tablename__ = "pasajeros"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)


class PasajeroVuelo(Base):
    __tablename__ = "pasajeros_vuelos"

    id = Column(Integer, primary_key=True, index=True)
    pasajero_id = Column(Integer, ForeignKey("pasajeros.id"))
    vuelo_id = Column(Integer, ForeignKey("vuelos.id"))
    peso_equipaje = Column(Integer)
