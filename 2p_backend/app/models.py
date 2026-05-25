from sqlalchemy import Integer, String, Text, DateTime, Enum as SAEnum, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base

import enum
from datetime import datetime


class Espacio(Base):
    __tablename__ = "espacios"

    # PK compuesta: (calle, numero)
    calle: Mapped[str] = mapped_column(String(120), primary_key=True)
    numero: Mapped[int] = mapped_column(Integer, primary_key=True)
    obs: Mapped[str] = mapped_column(Text, nullable=False)

class UsoEspacioEstado(str, enum.Enum):
    RESERVADO = "RESERVADO"
    FINALIZADO = "FINALIZADO"

class UsoEspacio(Base):
    __tablename__ = "usos_espacio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    espacio_calle: Mapped[str] = mapped_column(String(120), nullable=False)
    espacio_numero: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["espacio_calle", "espacio_numero"],
            ["espacios.calle", "espacios.numero"],
        ),
    )

    # relación ORM (opcional, pero útil)
    espacio: Mapped["Espacio"] = relationship("Espacio")

    chapa: Mapped[str] = mapped_column(String(20), nullable=False)
    inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    duracion: Mapped[int] = mapped_column(Integer, nullable=False)  # horas
    estado: Mapped[UsoEspacioEstado] = mapped_column(
        SAEnum(UsoEspacioEstado, name="uso_espacio_estado"),
        nullable=False,
        default=UsoEspacioEstado.RESERVADO,
    )
