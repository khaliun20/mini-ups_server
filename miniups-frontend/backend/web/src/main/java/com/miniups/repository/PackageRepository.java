package com.miniups.repository;

import com.miniups.entity.Packages;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PackageRepository extends JpaRepository<Packages, Integer> {

    Packages findByTruckingNum(int trackingNum);
    List<Packages> findByUsername(String name);
}