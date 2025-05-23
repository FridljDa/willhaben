package com.example.willhaben.listing.structure;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Listing {
    private static final Logger logger = Logger.getLogger(Listing.class.getName());
    private final Map<String, String> listingData;

    public Listing() {
        this.listingData = new HashMap<>();
    }

    /**
     * Pretty prints the listing details in JSON-like format.
     */
    public void prettyPrint() {
        System.out.println(listingData);
    }

    /**
     * Returns the listing details as a dictionary.
     * @return A map containing the listing details.
     */
    public Map<String, Optional<String>> getListingDict() {
        Map<String, Optional<String>> result = new HashMap<>();
        for (Map.Entry<String, String> entry : listingData.entrySet()) {
            result.put(entry.getKey(), Optional.ofNullable(entry.getValue()));
        }
        return result;
    }

    /**
     * Adds a key-value pair to the listing data.
     * @param key The key to add.
     * @param value The value to add.
     */
    public void addKeyValuePair(String key, String value) {
        updateDict(Map.of(key, value));
    }

    /**
     * Updates the listing data with the provided dictionary.
     * @param newListingData The dictionary to update.
     */
    public void updateDict(Map<String, String> newListingData) {
        for (Map.Entry<String, String> entry : newListingData.entrySet()) {
            String key = entry.getKey();
            String value = entry.getValue();
            if (key != null && value != null) {
                listingData.put(key, value);
            } else {
                logger.log(Level.FINE, "Key or value is null. Key: {0}, Value: {1}", new Object[]{key, value});
            }
        }
    }
}