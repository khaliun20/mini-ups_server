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
@Table(name = "Items")
public class Items {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Integer id;

    @Column(name = "trucking_num", nullable = false)
    private Integer truckingNum;

    @Column(name = "description")
    private String description;

    @Column(name = "quantity")
    private Integer quantity;

    // getters and setters
}
