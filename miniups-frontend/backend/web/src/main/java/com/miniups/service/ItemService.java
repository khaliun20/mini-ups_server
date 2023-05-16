package com.miniups.service;


import com.miniups.entity.Items;
import com.miniups.repository.ItemRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ItemService{

    private ItemRepository itemRepository;

    public ItemService(ItemRepository itemRepository) {
        this.itemRepository = itemRepository;
    }


    public List<Items> findItemsByTrackingNum(int trackingNum) {
        List<Items> items = itemRepository.findByTruckingNum(trackingNum);
        return items;
    }

    
}