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
@Table(name = "AmazonAck")
public class AmazonAck {
@Id
@Column(name = "ack", nullable = false)
private Integer ack;

// Constructor, getters, and setters

}
