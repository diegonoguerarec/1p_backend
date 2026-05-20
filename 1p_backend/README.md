# Sistema de reserva de fletes

## Modelado
Se tiene un modelo de Camiones y otro de Reservas. A una reserva le corresponde un solo camión y un camión puede estar en varias reservas.

Las reservas tienen fecha de inicio y de fin (fecha_desde y fecha_hasta).

Las validaciones incluyen
- Fecha de inicio debe ser antes que fecha de fin
- El camión asignado debe tener una capacidad mayor o igual al volumen a ser transportado
- El camíón debe estar sin reservas en las fechas de inicio y fin para poder ser asignado
- Camion no debe estar borrado

<br>

Endpoints sobre camiones
- GET /camiones listar todos los camiones
- GET /camiones/id listar camión por id
- POST /camiones crear camión
- PUT /camiones/id actualizar camión
- DELETE /camiones/id borrar camión (soft delete)
- GET /camiones/libres listar camiones libres por rango de fecha y volumen de carga

<br>

Endpoints sobre reservas
- GET /reservas listar todas las reservas
- POST /reservas crear reserva
- PATCH /reservas/cancelar/id marcar una reserva como cancelada

## Instrucciones para correr el proyecto
Tener instalado java, quarkus y docker (opcional para la base de datos).

Entrar en la carpeta code-with-quarkus.

1. Levantar el contenedor de postgres:
    ```
        docker run --name db_camiones \
        -e POSTGRES_USER=Admin \
        -e POSTGRES_PASSWORD=admin.1234 \
        -e POSTGRES_DB=empresa_fletes \
        -p 5432:5432 \
        -d postgres:15.17-trixie
    ```
    A partir de aqui para apagarlo/prenderlo:
    ```
    docker stop db_camiones
    docker start db_camiones
    ```

2. Correr el proyecto `./mvnw quarkus:dev`


