package com.miniups.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "WorldAck")
public class WorldAck {
    @Id
    @Column(name = "ack", nullable = false)
    private int ack;

    // Constructors, getters and setters
}