package com.miniups.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.miniups.entity.ShipLabel;

@Repository
public interface ShipLabelRepository extends JpaRepository<ShipLabel, Integer>{

    List<ShipLabel> findByUsername(String username);
}
