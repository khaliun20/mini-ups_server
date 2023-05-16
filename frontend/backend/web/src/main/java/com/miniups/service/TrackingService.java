package com.miniups.service;

import com.miniups.entity.Packages;
import com.miniups.repository.PackageRepository;
import org.springframework.stereotype.Service;



@Service
public class TrackingService{

    private PackageRepository packageRepository;

    public TrackingService(PackageRepository packageRepository) {
        this.packageRepository = packageRepository;
    }

    public Packages findPackageByTrackingNum(int trackingNum) {
        return packageRepository.findByTruckingNum(trackingNum);
    }


}