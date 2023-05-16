package com.miniups.repository;

import com.miniups.entity.Truck;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TruckRepository extends JpaRepository<Truck, Integer> {

    // Truck findById(int truckid);
}