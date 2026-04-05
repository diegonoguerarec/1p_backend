package service;

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
}