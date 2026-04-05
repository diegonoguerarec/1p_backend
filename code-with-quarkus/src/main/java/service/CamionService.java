package service;

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
}