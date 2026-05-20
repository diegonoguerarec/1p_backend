package resource;

import java.util.List;

import entity.Camion;
import jakarta.inject.Inject;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.QueryParam;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import service.CamionService;

@Path("/camiones")
@Consumes(MediaType.APPLICATION_JSON)
@Produces(MediaType.APPLICATION_JSON)
public class CamionResource {
    @Inject
    CamionService service;

    @GET
    public Response listar () {
        List<Camion> camiones = service.listarActivos();
        return Response.ok(camiones).build();
    }

    @GET
    @Path("/{id}")
    public Response consultarPorId (@PathParam("id") Long id) {
        Camion c = service.consultarPorId(id);

        if (c == null) {
            return Response.status(Response.Status.NOT_FOUND).build();
        } else {
            return Response.ok(c).build();
        }
    }

    @POST
    public Response crear (Camion camion) {
        service.crear(camion);
        return Response.status(Response.Status.CREATED).build();
    }

    @PUT
    @Path("/{id}")
    public Response actualizar (@PathParam("id") Long id, Camion camionActualizado) {
        boolean ok = service.actualizar(id, camionActualizado);
        
        if (ok) {
            return Response.ok(camionActualizado).build();
        } else {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
    }

    @DELETE
    @Path("/{id}")
    public Response borrar (@PathParam("id") Long id) {
        boolean ok = service.borrarLogico(id);

        if (ok) {
            return Response.noContent().build();
        } else {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
    }

    @GET
    @Path("/libres")
    public Response camionesLibresPorFecha (
        @QueryParam("fecha_desde") String fecha_desde,
        @QueryParam("fecha_hasta") String fecha_hasta,
        @QueryParam("volumen") double volumen
    ) {
        List<Camion> camionesLibres = service.camionesDisponiblesPorFechayVolumen(
            java.time.LocalDate.parse(fecha_desde),
            java.time.LocalDate.parse(fecha_hasta),
            volumen
        );

        return Response.ok(camionesLibres).build();
    }
}
