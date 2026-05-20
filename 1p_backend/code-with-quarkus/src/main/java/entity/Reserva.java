package entity;

import java.time.LocalDate;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

@Entity
public class Reserva {
    @Id
    @GeneratedValue
    private Long id;

    // Enlace con la entidad de Camiones
    @ManyToOne(optional = false)
    @JoinColumn(name = "camion_id", nullable = false)
    @NotNull
    private Camion camion;

    @NotNull
    private String origen;

    @NotNull
    private String destino;

    @NotNull
    private LocalDate fecha_desde;

    @NotNull
    private LocalDate fecha_hasta;

    @NotNull
    @Positive
    private double volumen_de_transporte;

    @NotNull
    private String estado; //PENDIENDE, APROVADO, CANCELADO, FINALIZADO

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getOrigen() {
        return origen;
    }

    public void setOrigen(String origen) {
        this.origen = origen;
    }

    public String getDestino() {
        return destino;
    }

    public void setDestino(String destino) {
        this.destino = destino;
    }

    public LocalDate getFecha_desde() {
        return fecha_desde;
    }

    public void setFecha_desde(LocalDate fecha_desde) {
        this.fecha_desde = fecha_desde;
    }

    public LocalDate getFecha_hasta() {
        return fecha_hasta;
    }

    public void setFecha_hasta(LocalDate fecha_hasta) {
        this.fecha_hasta = fecha_hasta;
    }
    
    public double getVolumen_de_transporte() {
        return volumen_de_transporte;
    }

    public void setVolumen_de_transporte(double volumen_de_transporte) {
        this.volumen_de_transporte = volumen_de_transporte;
    }

    public String getEstado() {
        return estado;
    }

    public void setEstado(String estado) {
        this.estado = estado;
    }

    public Camion getCamion() {
        return camion;
    }

    public void setCamion(Camion camion) {
        this.camion = camion;
    }
}
