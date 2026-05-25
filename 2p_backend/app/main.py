from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import Espacio as EspacioModel
from .schemas import Espacio, EspacioUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    ## Se puede reemplazar por migraciones
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

@app.post("/espacios", response_model=Espacio, status_code=status.HTTP_201_CREATED)
def crear_espacio(payload: Espacio, db: Session = Depends(get_db)):
    espacio = EspacioModel(**payload.model_dump())
    db.add(espacio)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un espacio con esa calle y número",
        )
    db.refresh(espacio)
    return espacio


@app.get("/espacios", response_model=List[Espacio])
def listar_espacios(db: Session = Depends(get_db)):
    stmt = select(EspacioModel).order_by(EspacioModel.calle, EspacioModel.numero)
    return db.scalars(stmt).all()


@app.get("/espacios/{calle}/{numero}", response_model=Espacio)
def obtener_espacio(calle: str, numero: int, db: Session = Depends(get_db)):
    espacio = db.get(EspacioModel, {"calle": calle, "numero": numero})
    if espacio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")
    return espacio


@app.put("/espacios/{calle}/{numero}", response_model=Espacio)
def actualizar_espacio(
    calle: str,
    numero: int,
    payload: EspacioUpdate,
    db: Session = Depends(get_db),
):
    espacio = db.get(EspacioModel, {"calle": calle, "numero": numero})
    if espacio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")

    espacio.obs = payload.obs
    db.commit()
    db.refresh(espacio)
    return espacio


@app.delete("/espacios/{calle}/{numero}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_espacio(calle: str, numero: int, db: Session = Depends(get_db)):
    espacio = db.get(EspacioModel, {"calle": calle, "numero": numero})
    if espacio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")

    db.delete(espacio)
    db.commit()
    return None
