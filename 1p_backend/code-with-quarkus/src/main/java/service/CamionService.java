package service;

import java.time.LocalDate;
import java.util.List;

import entity.Camion;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.transaction.Transactional;

@ApplicationScoped
public class CamionService {
    @Inject
    EntityManager em;

    @Transactional
    public void crear (Camion camion) {
        em.persist(camion);
    }
    
    @Transactional
    public boolean borrarLogico (Long id) {
        Camion camion = em.find(Camion.class, id);

        if (camion == null) {return false;} else {
            camion.setBorrado(true);
            return true;
        }
    }

    @Transactional
    public boolean actualizar (Long id, Camion camionActualizado) {
        Camion camion = em.find(Camion.class, id);

        if (camion == null) {return false;} else /*No se encontró un camion con esa id*/{
            camion.setChapa(camionActualizado.getChapa());
            camion.setCapacidad(camionActualizado.getCapacidad());
            camion.setMarca(camionActualizado.getMarca());
            camion.setModelo(camionActualizado.getModelo());
            camion.setAnio_fabricacion(camionActualizado.getAnio_fabricacion());
            return true;
        }
    }

    public List<Camion> listarActivos () {
        return em.createQuery("SELECT c FROM Camion c WHERE c.borrado = false", Camion.class)
            .getResultList();
    }

    public Camion consultarPorId (Long id) {
        Camion c = em.find(Camion.class, id);
        
        // Si no existe camion con esa id
        if (c == null) return null;

        // Si el camion está borrado
        if (c.getBorrado()) return null;

        // El camion existe y no está borrado
        return c;
    }

    public List<Camion> camionesDisponiblesPorFechayVolumen (LocalDate fecha_desde, LocalDate fecha_hasta, double volumen) {
        return em.createQuery(
            "SELECT c FROM Camion c WHERE c.borrado = false AND c.id NOT IN (" +
            "SELECT r.camion.id FROM Reserva r WHERE " +
            "(r.fecha_desde <= :fecha_hasta AND r.fecha_hasta >= :fecha_desde) AND r.estado IN ('PENDIENTE', 'APROBADO')" +
            ") AND c.capacidad_kg >= :volumen", Camion.class)
            .setParameter("fecha_desde", fecha_desde)
            .setParameter("fecha_hasta", fecha_hasta)
            .setParameter("volumen", volumen)
            .getResultList();
    }
}