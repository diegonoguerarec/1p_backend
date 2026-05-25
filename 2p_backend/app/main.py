from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import Espacio as EspacioModel
from .models import UsoEspacio as UsoEspacioModel, UsoEspacioEstado as UsoEspacioEstadoModel
from .schemas import Espacio, EspacioUpdate, UsoEspacio, UsoEspacioCreate


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

# Endpoints para Usos de Espacio
@app.post("/usos-espacio", response_model=UsoEspacio, status_code=status.HTTP_201_CREATED)
def crear_uso_espacio(payload: UsoEspacioCreate, db: Session = Depends(get_db)):
    # validar que el Espacio exista (así evitás IntegrityError por FK)
    espacio = db.get(EspacioModel, {"calle": payload.espacio_calle, "numero": payload.espacio_numero})
    if espacio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Espacio no encontrado")

    # Validación para evitar solapamientos
    existing_fin = UsoEspacioModel.inicio + func.make_interval(
    0, 0, 0, 0, UsoEspacioModel.duracion, 0, 0
    )

    stmt = (
        select(UsoEspacioModel.id)
        .where(
            UsoEspacioModel.espacio_calle == payload.espacio_calle,
            UsoEspacioModel.espacio_numero == payload.espacio_numero,
            UsoEspacioModel.estado == UsoEspacioEstadoModel.RESERVADO,
            UsoEspacioModel.inicio < existing_fin,
            existing_fin > payload.inicio,
        )
        .limit(1)
    )

    conflicto_id = db.execute(stmt).scalar_one_or_none()
    if conflicto_id is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El espacio ya está reservado en ese horario",
        )

    uso = UsoEspacioModel(
        espacio_calle=payload.espacio_calle,
        espacio_numero=payload.espacio_numero,
        chapa=payload.chapa,
        inicio=payload.inicio,
        duracion=payload.duracion,
        estado=UsoEspacioEstadoModel.RESERVADO,  # fuerza default según el enunciado
    )

    db.add(uso)
    db.commit()
    db.refresh(uso)
    return uso

@app.get("/usos-espacio/{uso_id}", response_model=UsoEspacio)
def obtener_uso_espacio(uso_id: int, db: Session = Depends(get_db)):
    uso = db.get(UsoEspacioModel, uso_id)
    if uso is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")
    return uso

@app.get("/usos-espacio", response_model=List[UsoEspacio])
def listar_usos_espacio(
    estado: Optional[UsoEspacioEstadoModel] = None,
    db: Session = Depends(get_db),
):
    stmt = select(UsoEspacioModel)

    if estado is not None:
        stmt = stmt.where(UsoEspacioModel.estado == estado)

    stmt = stmt.order_by(UsoEspacioModel.inicio.desc())
    return db.scalars(stmt).all()

@app.put("/usos-espacio/{uso_id}/finalizar", response_model=UsoEspacio)
def finalizar_uso_espacio(uso_id: int, db: Session = Depends(get_db)):
    uso = db.get(UsoEspacioModel, uso_id)
    if uso is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")

    if uso.estado != UsoEspacioEstadoModel.RESERVADO:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Solo se puede finalizar si está en estado RESERVADO",
        )

    uso.estado = UsoEspacioEstadoModel.FINALIZADO
    db.commit()
    db.refresh(uso)
    return uso
