from sqlalchemy.orm import object_mapper


def model_to_dict(model):
    mapper = object_mapper(model)
    data = {}
    for column in mapper.columns:
        value = getattr(model, column.key)
        data[column.key] = value
    return data


def calcular_duracion(fecha_salida, fecha_llegada):
    duracion = (fecha_llegada - fecha_salida).total_seconds() / 3600
    return duracion
