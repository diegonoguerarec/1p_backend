package entity;

import jakarta.persistence.*;

@Entity
public class Camion {
    @Id
    @GeneratedValue
    private Long id;

    private String chapa;

    private double capacidad;

    private String marca;

    private String modelo;

    private int anio_fabricacion;

    // Getters and Setters

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getChapa() {
        return chapa;
    }

    public void setChapa(String chapa) {
        this.chapa = chapa;
    }

    public void setCapacidad(double capacidad) {
        this.capacidad = capacidad;
    }

    public double getCapacidad() {
        return capacidad;
    }

    public String getMarca() {
        return marca;
    }

    public void setMarca(String marca) {
        this.marca = marca;
    }

    public String getModelo() {
        return modelo;
    }

    public void setModelo(String modelo) {
        this.modelo = modelo;
    }

    public int getAnio_fabricacion() {
        return anio_fabricacion;
    }

    public void setAnio_fabricacion(int anio_fabricacion) {
        this.anio_fabricacion = anio_fabricacion;
    }
}
