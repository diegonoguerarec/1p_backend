from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Espacio(Base):
    __tablename__ = "espacios"

    # PK compuesta: (calle, numero)
    calle: Mapped[str] = mapped_column(String(120), primary_key=True)
    numero: Mapped[int] = mapped_column(Integer, primary_key=True)
    obs: Mapped[str] = mapped_column(Text, nullable=False)
