from pydantic import BaseModel, ConfigDict, Field
import enum
from datetime import datetime

from .models import UsoEspacioEstado
# Modelos para serializar datos de entrada y salida de la API

class Espacio(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    calle: str
    numero: int
    obs: str


class EspacioUpdate(BaseModel):
    obs: str

class UsoEspacioCreate(BaseModel):
    espacio_calle: str
    espacio_numero: int
    chapa: str
    inicio: datetime
    duracion: int = Field(ge=1)
    estado: UsoEspacioEstado = UsoEspacioEstado.RESERVADO

class UsoEspacio(UsoEspacioCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


# -----------------
# Boleta (facturación)
# -----------------

class BoletaCreate(BaseModel):
    chapa: str
    fecha_inicio: datetime
    fecha_fin: datetime


class BoletaCabecera(BaseModel):
    fecha_emision: datetime
    chapa: str
    total_a_pagar: int


class BoletaEspacioUsado(BaseModel):
    calle: str
    numero: int


class BoletaDetalleItem(BaseModel):
    espacio_usado: BoletaEspacioUsado
    fecha_hora_inicio: datetime
    fecha_hora_finalizacion: datetime
    cantidad_horas_utilizadas: int
    monto_por_hora: int
    total_a_pagar: int


class BoletaResponse(BaseModel):
    cabecera: BoletaCabecera
    detalle: list[BoletaDetalleItem]
