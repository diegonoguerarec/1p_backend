package resource;

import java.util.List;

import entity.Reserva;
import jakarta.inject.Inject;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.PATCH;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import service.ReservaService;

@Path("/reservas")
@Consumes(MediaType.APPLICATION_JSON)
@Produces(MediaType.APPLICATION_JSON)
public class ReservaResource {
    @Inject
    ReservaService service;

    @GET
    public Response listar () {
        List<Reserva> reservas = service.listar();
        return Response.ok(reservas).build();
    }

    @POST
    public Response crear (Reserva reserva) {
        service.crear(reserva);

        return Response.status(Response.Status.CREATED).build();
    }

    @PATCH
    @Path("/cancelar/{id}")
    public Response cancelar (@PathParam("id") Long id) {
        service.cancelar(id);

        return Response.ok().build();
    }
}