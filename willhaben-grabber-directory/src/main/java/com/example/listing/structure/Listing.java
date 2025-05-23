package com.example.willhaben.listing.structure;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.logging.Level;
import java.util.logging.Logger;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;

@Entity //TODO what does this do?
@Table(name = "Listing")
public class Listing {
    private static final Logger logger = Logger.getLogger(Listing.class.getName());
    private final Map<String, String> listingData;
    //private date AVAILABLE_DATE;

    public Listing() {
        this.listingData = new HashMap<>();
    }


}