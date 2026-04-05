package resource;

import java.util.List;

import entity.Reserva;
import jakarta.inject.Inject;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
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
}
