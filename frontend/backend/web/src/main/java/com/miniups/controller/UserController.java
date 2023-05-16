package com.miniups.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.miniups.entity.User;
import com.miniups.service.UserService;

@RestController
@CrossOrigin
@RequestMapping("/api/users")
public class UserController {

    @Autowired
    private UserService userService;

    @PostMapping("")
    public ResponseEntity<User> createUser(@RequestBody User user) {
        User exist_user =  userService.getUserByName(user.getUsername());
        System.out.print("1111111111111");
        if(exist_user != null){
            return new ResponseEntity<User>(user, HttpStatus.CONFLICT);
        }else{
            return  new ResponseEntity<User>(userService.createUser(user), HttpStatus.OK);
        }
    }

    @GetMapping("/{username}")
    public ResponseEntity<User> getUserById(@PathVariable String username) {

        User user = userService.getUserByName(username);
        if(user == null){
            return new ResponseEntity<User>(user, HttpStatus.NOT_FOUND);
        }else{
            return new ResponseEntity<User>(user, HttpStatus.OK);
        }
    }
}
