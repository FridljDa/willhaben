package de.danielfridljand.willhaben.listing.structure;

import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.HashMap;
import java.util.Map;

@Data
@NoArgsConstructor
public class SingleListing {
    
    private Map<String, Object> properties = new HashMap<>();
    
    /**
     * Adds a key-value pair to the listing properties.
     *
     * @param key   The property key
     * @param value The property value
     */
    public void addKeyValuePair(String key, Object value) {
        properties.put(key, value);
    }
    
    /**
     * Gets a property value by key.
     *
     * @param key The property key
     * @return The property value, or null if not found
     */
    public Object getProperty(String key) {
        return properties.get(key);
    }
    
    /**
     * Checks if a property exists.
     *
     * @param key The property key
     * @return true if the property exists, false otherwise
     */
    public boolean hasProperty(String key) {
        return properties.containsKey(key);
    }
} 