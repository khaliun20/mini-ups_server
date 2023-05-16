package com.miniups.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.miniups.entity.Branches;

public interface BranchesRepository extends JpaRepository<Branches, Integer>  {
    
}
