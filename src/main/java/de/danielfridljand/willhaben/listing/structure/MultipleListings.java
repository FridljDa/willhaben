package de.danielfridljand.willhaben.listing.structure;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class MultipleListings {
    
    private List<SingleListing> listings = new ArrayList<>();
    private Path path;
    
    /**
     * Constructor with path parameter.
     *
     * @param path The file path for storing/loading listings
     */
    public MultipleListings(Path path) {
        this.listings = new ArrayList<>();
        this.path = path;
    }
    
    /**
     * Appends a single listing to the collection.
     *
     * @param listing The listing to append
     */
    public void appendListing(SingleListing listing) {
        listings.add(listing);
    }
    
    /**
     * Gets the number of listings.
     *
     * @return The number of listings
     */
    public int size() {
        return listings.size();
    }
    
    /**
     * Gets a listing by index.
     *
     * @param index The index of the listing
     * @return The listing at the specified index
     */
    public SingleListing getListing(int index) {
        return listings.get(index);
    }
    
    /**
     * Gets all listings.
     *
     * @return A list of all listings
     */
    public List<SingleListing> getAllListings() {
        return new ArrayList<>(listings); // Return a copy to preserve encapsulation
    }
    
    /**
     * Clears all listings.
     */
    public void clear() {
        listings.clear();
    }
    
    /**
     * Checks if the collection is empty.
     *
     * @return true if empty, false otherwise
     */
    public boolean isEmpty() {
        return listings.isEmpty();
    }
    
    /**
     * Pretty prints all listings in a formatted, readable way.
     * Displays each listing with its properties organized and easy to read.
     */
    public void prettyPrint() {
        System.out.println("═".repeat(80));
        System.out.println("                       LISTINGS OVERVIEW");
        System.out.println("═".repeat(80));
        System.out.printf("Total Listings: %d%n", listings.size());
        if (path != null) {
            System.out.printf("Path: %s%n", path.toString());
        }
        System.out.println("═".repeat(80));
        
        if (listings.isEmpty()) {
            System.out.println("No listings available.");
            System.out.println("═".repeat(80));
            return;
        }
        
        for (int i = 0; i < listings.size(); i++) {
            SingleListing listing = listings.get(i);
            System.out.printf("%n┌─ LISTING %d %s%n", i + 1, "─".repeat(65));
            
            Map<String, Object> properties = listing.getProperties();
            if (properties.isEmpty()) {
                System.out.println("│  No properties available");
            } else {
                // Print URL first if available (most important property)
                if (properties.containsKey("url")) {
                    System.out.printf("│  %-20s: %s%n", "URL", formatValue(properties.get("url")));
                }
                
                // Print other properties in alphabetical order (except url)
                properties.entrySet().stream()
                    .filter(entry -> !"url".equals(entry.getKey()))
                    .sorted(Map.Entry.comparingByKey())
                    .forEach(entry -> {
                        String key = entry.getKey();
                        Object value = entry.getValue();
                        System.out.printf("│  %-20s: %s%n", truncateKey(key), formatValue(value));
                    });
            }
            
            System.out.printf("└%s%n", "─".repeat(73));
        }
        
        System.out.println("═".repeat(80));
    }
    
    /**
     * Returns a pretty formatted string representation of all listings.
     *
     * @return A formatted string containing all listings
     */
    public String prettyPrintToString() {
        StringBuilder sb = new StringBuilder();
        sb.append("═".repeat(80)).append("\n");
        sb.append("                       LISTINGS OVERVIEW\n");
        sb.append("═".repeat(80)).append("\n");
        sb.append(String.format("Total Listings: %d%n", listings.size()));
        if (path != null) {
            sb.append(String.format("Path: %s%n", path.toString()));
        }
        sb.append("═".repeat(80)).append("\n");
        
        if (listings.isEmpty()) {
            sb.append("No listings available.\n");
            sb.append("═".repeat(80)).append("\n");
            return sb.toString();
        }
        
        for (int i = 0; i < listings.size(); i++) {
            SingleListing listing = listings.get(i);
            sb.append(String.format("%n┌─ LISTING %d %s%n", i + 1, "─".repeat(65)));
            
            Map<String, Object> properties = listing.getProperties();
            if (properties.isEmpty()) {
                sb.append("│  No properties available\n");
            } else {
                // Print URL first if available
                if (properties.containsKey("url")) {
                    sb.append(String.format("│  %-20s: %s%n", "URL", formatValue(properties.get("url"))));
                }
                
                // Print other properties in alphabetical order (except url)
                properties.entrySet().stream()
                    .filter(entry -> !"url".equals(entry.getKey()))
                    .sorted(Map.Entry.comparingByKey())
                    .forEach(entry -> {
                        String key = entry.getKey();
                        Object value = entry.getValue();
                        sb.append(String.format("│  %-20s: %s%n", truncateKey(key), formatValue(value)));
                    });
            }
            
            sb.append(String.format("└%s%n", "─".repeat(73)));
        }
        
        sb.append("═".repeat(80));
        return sb.toString();
    }
    
    /**
     * Formats a value for display, handling null values and long strings.
     *
     * @param value The value to format
     * @return A formatted string representation of the value
     */
    private String formatValue(Object value) {
        if (value == null) {
            return "<null>";
        }
        
        String stringValue = value.toString();
        
        // Truncate very long strings
        if (stringValue.length() > 100) {
            return stringValue.substring(0, 97) + "...";
        }
        
        // Handle empty strings
        if (stringValue.trim().isEmpty()) {
            return "<empty>";
        }
        
        return stringValue;
    }
    
    /**
     * Truncates property keys if they're too long for display.
     *
     * @param key The property key
     * @return A truncated key if necessary
     */
    private String truncateKey(String key) {
        if (key.length() > 20) {
            return key.substring(0, 17) + "...";
        }
        return key;
    }
} 