package com.miniups.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

// import com.miniups.*;



@Setter
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "Packages")
public class Packages {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "packages_id")
    private Integer packagesId;

    @Column(name = "truck_id")
    private Integer truckId;

    @Column(name = "trucking_num", nullable = false)
    private Integer truckingNum;

    @Column(name = "x", nullable = false)
    private Integer x;

    @Column(name = "y", nullable = false)
    private Integer y;

    @Column(name = "username")
    private String username;

    @Column(name = "warehouse_id", nullable = false)
    private Integer warehouseId;

    @Column(name = "state", nullable = false)
    private String state;

    // constructors, getters and setters omitted for brevity

    // public enum PackageState {
    //     delivering, 
    //     preparing_for_pickup,
    //     delivered,
    //     arrive_warehouse, 
    //     loading, 
    //     loaded,
    //     ready_for_pickup
    // }
}