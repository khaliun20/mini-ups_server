package com.miniups.repository;

import com.miniups.entity.Items;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ItemRepository extends JpaRepository<Items, Integer> {

    List<Items> findByTruckingNum(int trackingNum);
}