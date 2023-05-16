package com.miniups.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.miniups.entity.ShipLabel;
import com.miniups.repository.ShipLabelRepository;

@Service
public class ShipLabelService {
    @Autowired
    private ShipLabelRepository shiplabelRepository;

    public ShipLabel createShipLabel(ShipLabel shiplabel) {
        return shiplabelRepository.save(shiplabel);
    }

    public List<ShipLabel> findAllLabelsByUsername(String name)  {
        return shiplabelRepository.findByUsername(name);
    }

}
