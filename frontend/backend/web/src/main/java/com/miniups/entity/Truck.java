package com.miniups.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;


@Setter
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "Truck")
public class Truck {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "truck_id")
    private Integer truckId;

    @Column(name = "x", nullable = false)
    private Integer x;

    @Column(name = "y", nullable = false)
    private Integer y;

    @Column(name = "wid")
    private Integer wid;

    @Enumerated(EnumType.STRING)
    @Column(name = "state", nullable = false)
    private TruckState state;

    @Enumerated(EnumType.STRING)
    @Column(name = "world_given_state", nullable = false)
    private TruckState worldGivenState;

    // Getters and setters


}



