package com.miniups.entity;

import com.fasterxml.jackson.annotation.JsonFormat;

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
@Table(name = "Shiplabel")
public class ShipLabel {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(nullable = false)
    private Integer tox;

    @Column(nullable = false)
    private Integer toy;

    @Column(nullable = false)
    private Integer fromx;

    @Column(nullable = false)
    private Integer fromy;

    @Column(nullable = false)
    private Double weight;

    @Column(nullable = false)
    private String username;

}

