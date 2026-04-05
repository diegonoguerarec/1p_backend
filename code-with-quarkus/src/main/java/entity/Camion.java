package entity;

import org.hibernate.annotations.ColumnDefault;

import io.smallrye.common.constraint.NotNull;
import jakarta.persistence.*;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Positive;

@Entity
public class Camion {
    @Id
    @GeneratedValue
    private Long id;

    @Column(unique = true)
    private String chapa;

    @NotNull
    @Positive
    private double capacidad_kg;

    private String marca;

    private String modelo;

    @Min(value = 2000)
    @Max(value = 2026)
    private int anio_fabricacion;

    // Para indicar borrado lógico
    @ColumnDefault("False")
    private boolean borrado;

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
        this.capacidad_kg = capacidad;
    }

    public double getCapacidad() {
        return capacidad_kg;
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

    public Boolean getBorrado() {
        return borrado;
    }

    public void setBorrado(Boolean borrado) {
        this.borrado = borrado;
    }
}
