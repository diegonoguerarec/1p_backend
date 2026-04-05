package service;

import java.util.List;

import entity.Reserva;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;

@ApplicationScoped
public class ReservaService {
    @Inject
    EntityManager em;

    // Lista todas las reservas
    public List<Reserva> listar () {
        return em.createQuery("SELECT r FROM Reserva r", Reserva.class)
            .getResultList();
    }
}
