package com.miniups.controller;

import com.miniups.entity.Packages;
import com.miniups.repository.PackageRepository;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
@CrossOrigin
public class LocationController {


    private PackageRepository packageRepository;

    public LocationController(PackageRepository packageRepository) {

        this.packageRepository = packageRepository;


    }

        @PostMapping(path = "/location/{trackingNum}/{x}/{y}")
        @ResponseBody
        public ResponseEntity<Packages> tracking(@PathVariable int trackingNum,@PathVariable int x, @PathVariable int y) {
            Packages packages = packageRepository.findByTruckingNum(trackingNum);
            packages.setX(x);
            packages.setY(y);
            packageRepository.save(packages);

            return new ResponseEntity<>(packages,HttpStatus.OK);
        }

}
