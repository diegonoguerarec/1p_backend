package service;

import java.time.LocalDate;
import java.util.List;
import org.jboss.logging.Logger;

import entity.Camion;
import entity.Reserva;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.BadRequestException;

@ApplicationScoped
public class ReservaService {
    @Inject
    EntityManager em;

    private static final Logger LOG = Logger.getLogger(ReservaService.class);

    // Lista todas las reservas
    public List<Reserva> listar () {
        return em.createQuery("SELECT r FROM Reserva r", Reserva.class)
            .getResultList();
    }

    @Transactional
    public void crear (Reserva reserva) {
        // Validaciones y creacion o error

        Long camion_id = reserva.getCamion().getId();
        Camion camion = em.find(Camion.class, camion_id);

        // Validaciones sobre el camion de la reserva
        if (camion == null) {
            LOG.warnf("El camión no existe");
            throw new BadRequestException("El camión especificado no existe");
        } else if (camion.getBorrado() == true) {
            LOG.warnf("El camión está borrado");
            throw new BadRequestException("El camión especificado está borrado");
        } else if (camion.getCapacidad() < reserva.getVolumen_de_transporte()) {
            LOG.warnf("La capacidad del camión es insuficiente");
            throw new BadRequestException("La capacidad del camión es insuficiente");
        }

        //Validar que las fechas no sean incorrectas
        LocalDate desde = reserva.getFecha_desde();
        LocalDate hasta = reserva.getFecha_hasta();

        if (!desde.isBefore(hasta)) {
            LOG.warnf("Las fechas de la reserva son incorrectas");
            throw new BadRequestException("Las fechas de la reserva son incorrectas");
        }

        // Validar que el camion no tenga otras reservas en ese rango de fecha
        // Si tiene una reserva PENDIENTE o APROBADA no se puede crear la reserva
        // Si tiene una reserva CANCELADA se puede crear
        Long conflictos = em.createQuery("SELECT COUNT(r) FROM Reserva r WHERE r.camion.id = :camionId AND r.estado IN ('PENDIENTE', 'APROBADA') AND r.fecha_desde <= :hasta AND r.fecha_hasta >= :desde", Long.class)
            .setParameter("camionId", camion_id)
            .setParameter("desde", desde)
            .setParameter("hasta", hasta).
            getSingleResult();

        if (conflictos > 0) {
            LOG.warnf("Ya hay una reserva que se solapa");
            throw new BadRequestException("Ya hay una reserva que se solapa");
        }

        // Siempre se crea una en estado pendiente
        reserva.setEstado("PENDIENTE");

        reserva.setCamion(camion);

        em.persist(reserva);
        
        LOG.infof("Reserva creada camion=%d desde=%s hasta=%s", camion_id, desde, hasta);
    }
}
