package com.miniups.controller;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import com.miniups.entity.ShipLabel;
import com.miniups.service.ShipLabelService;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;


@RestController
@CrossOrigin
public class ShipLabelController {
    
    private ShipLabelService shiplabelService;

    public ShipLabelController(ShipLabelService shiplabelService){
        this.shiplabelService = shiplabelService;
    }

    @GetMapping(path = "/labels/{username}")
    @ResponseBody
    @CrossOrigin
    public ResponseEntity<List<ShipLabel>> getAllShipLabelsFromUsername(@PathVariable String username){
        List<ShipLabel> shiplabels = shiplabelService.findAllLabelsByUsername(username);
        return new ResponseEntity<List<ShipLabel>>(shiplabels, HttpStatus.OK);
    }


    @PostMapping(path = "/labels")
    public ResponseEntity<ShipLabel> createShipLabel(@RequestBody ShipLabel shiplabel) {
        shiplabelService.createShipLabel(shiplabel);
        return new ResponseEntity<ShipLabel>(shiplabel, HttpStatus.OK);
    }
    

}
