def model_to_dict(model):
    mapper = object_mapper(model)
    data = {}
    for column in mapper.columns:
        value = getattr(model, column.key)
        data[column.key] = value
    return data
