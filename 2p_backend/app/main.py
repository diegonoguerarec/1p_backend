from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, func, exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from .db import Base, engine, get_db
from .models import Espacio as EspacioModel
from .models import UsoEspacio as UsoEspacioModel, UsoEspacioEstado as UsoEspacioEstadoModel
from .schemas import (
    Espacio,
    EspacioUpdate,
    UsoEspacio,
    UsoEspacioCreate,
    BoletaCreate,
    BoletaResponse,
    BoletaDetalleItem,
    BoletaCabecera,
    BoletaEspacioUsado,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    ## Se puede reemplazar por migraciones
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

MONTO_POR_HORA = 10

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
    # validar que el Espacio exista
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
        estado=UsoEspacioEstadoModel.RESERVADO,
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

@app.get("/espacios/disponibles", response_model=List[Espacio])
def listar_espacios_disponibles(
    inicio: datetime,
    fin: datetime,
    db: Session = Depends(get_db),
):
    if fin <= inicio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parámetro fin debe ser mayor que inicio",
        )

    uso_fin = UsoEspacioModel.inicio + func.make_interval(
        0, 0, 0, 0, UsoEspacioModel.duracion, 0, 0
    )

    ocupado = exists(
        select(1).where(
            UsoEspacioModel.espacio_calle == EspacioModel.calle,
            UsoEspacioModel.espacio_numero == EspacioModel.numero,
            UsoEspacioModel.estado == UsoEspacioEstadoModel.RESERVADO,
            UsoEspacioModel.inicio < fin,
            uso_fin > inicio,
        )
    )

    stmt = (
        select(EspacioModel)
        .where(~ocupado)
        .order_by(EspacioModel.calle, EspacioModel.numero)
    )
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

@app.post("/generar-boleta", response_model=BoletaResponse)
def generar_boleta(payload: BoletaCreate, db: Session = Depends(get_db)):
    if payload.fecha_fin <= payload.fecha_inicio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha_fin debe ser mayor que la fecha_inicio",
        )

    # Se incluye cualquier uso que se solape con el rango solicitado.
    uso_fin_expr = UsoEspacioModel.inicio + func.make_interval(
        0, 0, 0, 0, UsoEspacioModel.duracion, 0, 0
    )

    stmt = (
        select(UsoEspacioModel)
        .options(joinedload(UsoEspacioModel.espacio))
        .where(
            UsoEspacioModel.chapa == payload.chapa,
            UsoEspacioModel.estado == UsoEspacioEstadoModel.FINALIZADO,
            UsoEspacioModel.inicio < payload.fecha_fin,
            uso_fin_expr > payload.fecha_inicio,
        )
        .order_by(UsoEspacioModel.inicio.asc())
    )

    usos = db.scalars(stmt).all()

    detalle: list[BoletaDetalleItem] = []
    total_boleta = 0
    for uso in usos:
        fin = uso.inicio + timedelta(hours=uso.duracion)
        total = int(uso.duracion) * MONTO_POR_HORA
        total_boleta += total
        detalle.append(
            BoletaDetalleItem(
                espacio_usado=BoletaEspacioUsado(
                    calle=uso.espacio_calle,
                    numero=uso.espacio_numero,
                ),
                fecha_hora_inicio=uso.inicio,
                fecha_hora_finalizacion=fin,
                cantidad_horas_utilizadas=int(uso.duracion),
                monto_por_hora=MONTO_POR_HORA,
                total_a_pagar=total,
            )
        )

    return BoletaResponse(
        cabecera=BoletaCabecera(
            fecha_emision=datetime.now(tz=timezone.utc),
            chapa=payload.chapa,
            total_a_pagar=total_boleta,
        ),
        detalle=detalle,
    )
