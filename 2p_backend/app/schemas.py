from pydantic import BaseModel, ConfigDict
# Modelos para serializar datos de entrada y salida de la API

class Espacio(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    calle: str
    numero: int
    obs: str


class EspacioUpdate(BaseModel):
    obs: str
