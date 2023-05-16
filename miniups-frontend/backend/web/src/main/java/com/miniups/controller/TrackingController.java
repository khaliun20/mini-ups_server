package com.miniups.controller;

import com.miniups.entity.Items;
import com.miniups.entity.Packages;
import com.miniups.entity.Truck;
import com.miniups.repository.PackageRepository;
import com.miniups.repository.TruckRepository;
import com.miniups.service.ItemService;
import com.miniups.service.TrackingService;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@CrossOrigin
public class TrackingController {

    private TrackingService trackingService;
    private ItemService itemService;
    private PackageRepository packageRepository;
    private TruckRepository truckRepository;


    public TrackingController(TruckRepository truckRepository,TrackingService trackingService,ItemService itemService,PackageRepository packageRepository) {
        this.trackingService = trackingService;
        this.itemService = itemService;
        this.packageRepository = packageRepository;
        this.truckRepository = truckRepository;

    }


    @GetMapping(path = "/packages/{trackingNum}")
    @ResponseBody
    @CrossOrigin
    public ResponseEntity<List<Packages>> getPackgefromTrackingNumber(@PathVariable int trackingNum) {
        System.out.print("！！！！！！！！！！！");
        Packages packages =trackingService.findPackageByTrackingNum(trackingNum);
        List<Packages> res = new ArrayList<>();
        res.add(packages);
        if(packages != null){
            return new ResponseEntity<>(res, HttpStatus.OK);
        }else{
            return new ResponseEntity<>(res, HttpStatus.NOT_FOUND);
        }
        
    }

    @GetMapping(path = "/trucks/{trackingNum}")
    @ResponseBody
    public ResponseEntity<Truck> getTruckFromTrackingNumber(@PathVariable int trackingNum) {
        Packages packages =trackingService.findPackageByTrackingNum(trackingNum);

        Optional<Truck> truck = truckRepository.findById(packages.getTruckId());

        return new ResponseEntity<>(truck.get(), HttpStatus.OK);
    }

    @GetMapping(path = "/{username}/packages")
    @ResponseBody
    public ResponseEntity<List<Packages> > getPackgesFromUsername(@PathVariable String username) {
        List<Packages> packages =packageRepository.findByUsername(username);
        return new ResponseEntity<>(packages, HttpStatus.OK);
    }

    @PostMapping(path = "/{username}/packages/{trackingNum}")
    @ResponseBody
    public ResponseEntity<Packages> addNewPackageForUser(@PathVariable String username, @PathVariable int trackingNum) {
        Packages packages = trackingService.findPackageByTrackingNum(trackingNum);
        if(packages != null){
            
           
            packages.setUsername(username);
            packageRepository.save(packages);
           
            return new ResponseEntity<>(packages, HttpStatus.OK);
        }else{
            return new ResponseEntity<>(packages, HttpStatus.NOT_FOUND);
        }
    }


    @GetMapping(path = "/{trackingNum}/items")
    @ResponseBody
    public ResponseEntity<List<Items> > getAllItemsFromTrackingNum(@PathVariable int trackingNum) {
        List<Items> items  =itemService.findItemsByTrackingNum(trackingNum);
        return new ResponseEntity<>(items, HttpStatus.OK);
    }

}
