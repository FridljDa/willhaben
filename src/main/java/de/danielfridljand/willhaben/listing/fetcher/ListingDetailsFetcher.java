package de.danielfridljand.willhaben.listing.fetcher;

import com.fasterxml.jackson.databind.JsonNode;
import de.danielfridljand.willhaben.listing.structure.SingleListing;
import lombok.extern.slf4j.Slf4j;

import java.io.IOException;
import java.net.http.HttpTimeoutException;

/**
 * Fetches and processes details for a single listing.
 */
@Slf4j
public class ListingDetailsFetcher extends Fetcher {
    
    private final SingleListing singleListing;
    
    /**
     * Initializes the fetcher with a SingleListing that contains a URL.
     *
     * @param singleListingWithUrl A SingleListing object that must contain a 'url' property
     * @throws IllegalArgumentException if the SingleListing doesn't contain a URL
     */
    public ListingDetailsFetcher(SingleListing singleListingWithUrl) {
        super(extractUrl(singleListingWithUrl));
        this.singleListing = singleListingWithUrl;
    }
    
    /**
     * Extracts the URL from a SingleListing object.
     *
     * @param singleListing The SingleListing object
     * @return The URL as a String
     * @throws IllegalArgumentException if the URL is not found or invalid
     */
    private static String extractUrl(SingleListing singleListing) {
        Object urlProperty = singleListing.getProperty("url");
        if (urlProperty == null) {
            throw new IllegalArgumentException("SingleListing must contain a 'url' property");
        }
        
        String url = urlProperty.toString();
        if (url.trim().isEmpty()) {
            throw new IllegalArgumentException("URL property cannot be empty");
        }
        
        return url;
    }
    
    /**
     * Extracts and sets the listing details from the fetched JSON data.
     * Populates the SingleListing object with all available attributes.
     */
    public void fetchAndSetSingleListingContent() {
        log.info("Fetching detailed content for listing from: {}", getUrl());
        
        try {
            JsonNode parsedData = fetchContentAsJson();
            
            // Navigate to listing attributes: props.pageProps.advertDetails.attributes.attribute
            JsonNode listingAttributes = extractListingAttributes(parsedData);
            
            if (listingAttributes == null || !listingAttributes.isArray()) {
                log.error("No listing attributes found in the JSON data for URL: {}", getUrl());
                return;
            }
            
            int attributeCount = 0;
            // Process each attribute
            for (JsonNode listingAttributeKeyValue : listingAttributes) {
                processListingAttribute(listingAttributeKeyValue);
                attributeCount++;
            }
            
            log.info("Successfully processed {} attributes for listing: {}", attributeCount, getUrl());
            
        } catch (HttpTimeoutException timeoutEx) {
            log.error("HTTP timeout occurred while fetching listing details for {}: {}", getUrl(), timeoutEx.getMessage());
        } catch (IOException ioEx) {
            log.error("IO error occurred while fetching listing details for {}: {}", getUrl(), ioEx.getMessage(), ioEx);
        } catch (Exception e) {
            log.error("An unexpected error occurred while fetching listing details for {}: {}", getUrl(), e.getMessage(), e);
        }
    }
    
    /**
     * Extracts listing attributes from the parsed JSON data.
     *
     * @param parsedData The parsed JSON data
     * @return JsonNode containing the listing attributes array, or null if not found
     */
    private JsonNode extractListingAttributes(JsonNode parsedData) {
        try {
            JsonNode props = parsedData.get("props");
            if (props == null) {
                log.error("Missing 'props' key in JSON data for URL: {}", getUrl());
                return null;
            }
            
            JsonNode pageProps = props.get("pageProps");
            if (pageProps == null) {
                log.error("Missing 'pageProps' key in JSON data for URL: {}", getUrl());
                return null;
            }
            
            JsonNode advertDetails = pageProps.get("advertDetails");
            if (advertDetails == null) {
                log.error("Missing 'advertDetails' key in JSON data for URL: {}", getUrl());
                return null;
            }
            
            JsonNode attributes = advertDetails.get("attributes");
            if (attributes == null) {
                log.error("Missing 'attributes' key in JSON data for URL: {}", getUrl());
                return null;
            }
            
            JsonNode attributeArray = attributes.get("attribute");
            if (attributeArray == null) {
                log.error("Missing 'attribute' array in JSON data for URL: {}", getUrl());
                return null;
            }
            
            return attributeArray;
            
        } catch (Exception e) {
            log.error("Failed to extract listing attributes for URL {}: {}", getUrl(), e.getMessage(), e);
            return null;
        }
    }
    
    /**
     * Processes a single listing attribute and adds it to the SingleListing object.
     *
     * @param listingAttributeKeyValue The JSON node containing the attribute data
     */
    private void processListingAttribute(JsonNode listingAttributeKeyValue) {
        try {
            // Get the attribute name
            JsonNode nameNode = listingAttributeKeyValue.get("name");
            if (nameNode == null || !nameNode.isTextual()) {
                log.warn("Missing or invalid 'name' field in listing attribute for URL: {}", getUrl());
                return;
            }
            
            String attributeName = nameNode.asText();
            
            // Get the values array
            JsonNode valuesArray = listingAttributeKeyValue.get("values");
            if (valuesArray == null || !valuesArray.isArray() || valuesArray.isEmpty()) {
                log.debug("Missing or empty 'values' array for attribute '{}' in URL: {}", attributeName, getUrl());
                return;
            }
            
            // Get the first value (index 0)
            JsonNode firstValue = valuesArray.get(0);
            if (firstValue == null) {
                log.debug("First value is null for attribute '{}' in URL: {}", attributeName, getUrl());
                return;
            }
            
            // Convert the value to appropriate type
            Object value;
            if (firstValue.isTextual()) {
                value = firstValue.asText();
            } else if (firstValue.isNumber()) {
                if (firstValue.isDouble() || firstValue.isFloat()) {
                    value = firstValue.asDouble();
                } else {
                    value = firstValue.asLong();
                }
            } else if (firstValue.isBoolean()) {
                value = firstValue.asBoolean();
            } else {
                value = firstValue.toString();
            }
            
            // Add the attribute to the single listing
            singleListing.addKeyValuePair(attributeName, value);
            log.debug("Added attribute '{}' with value '{}' for URL: {}", attributeName, value, getUrl());
            
        } catch (Exception e) {
            log.error("Error processing listing attribute for URL {}: {}", getUrl(), e.getMessage(), e);
        }
    }
} 