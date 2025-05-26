package de.danielfridljand.willhaben.listing.datamodel;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.logging.Level;
import java.util.logging.Logger;

import jakarta.persistence.Entity;
import jakarta.persistence.Table; //TODO org.hibernate.orm instead?

@Entity //TODO what does this do?
@Table(name = "Listing")
//TODO @toString(exclude = {}) //lombok
public class Listing {
    //private date AVAILABLE_DATE;

    public Listing() {

    }

}