package de.danielfridljand.willhaben.listing.datamodel;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ListingRepository extends JpaRepository<Listing, Long> {
    // You can add custom query methods here if needed
    // For example:
    // List<Listing> findByPropertyName(String propertyName);
} 