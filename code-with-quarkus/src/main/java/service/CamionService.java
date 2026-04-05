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
}