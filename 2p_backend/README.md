## Iniciar contenedor de la base de datos
La primea vez ejecutar:
```
    docker run --name db_estacionamiento \
    -e POSTGRES_USER=Admin \
    -e POSTGRES_PASSWORD=admin.1234 \
    -e POSTGRES_DB=estacionamiento \
    -p 5432:5432 \
    -d postgres:15.17-trixie
```

Luego para apagarlo y prenderlo respectivamente:
```
    docker stop db_estacionamiento
    docker start db_estacionamiento
```

## Iniciar la app
Activar venv (recomendado)
```
    source venv/bin/activate
```

Instalar dependencias
```
    pip install -r requirements.txt
```

Iniciar la app
```
    uvicorn main:app --reload
```

## Modelo de datos

Se tiene una tabla de Espacios que representa cada espacio disponible. Tiene una PK compuesta por la calle y el número del espacio. La tabla UsoEspacio hace referencia a la tabla espacios y representa una reserva, contiene la chapa del vehiculo, un tiempo de inicio y duración.

![Diagrama de Tablas](/2p_backend/img/image.png)

## Endpoints disponibles

![Lista de Endpoints](/2p_backend/img/image-1.png)

Para consultar el swagger dirigirse a localhost:8000/docs con el proyecto corriendo.