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