package de.danielfridljand.willhaben.listing.fetcher;

import com.fasterxml.jackson.databind.JsonNode;
import de.danielfridljand.willhaben.listing.structure.MultipleListings;
import de.danielfridljand.willhaben.listing.structure.SingleListing;
import lombok.extern.slf4j.Slf4j;

import java.io.IOException;
import java.net.http.HttpTimeoutException;

/**
 * Fetches and processes listings from a given URL.
 */
@Slf4j
public class ListingsOverviewFetcher extends Fetcher {
    
    // Constants for JSON keys
    private static final String KEY_PROPS = "props";
    private static final String KEY_PAGE_PROPS = "pageProps";
    private static final String KEY_SEARCH_RESULT = "searchResult";
    private static final String KEY_LISTING_SUMMARY_LIST = "advertSummaryList";
    private static final String KEY_LISTING_SUMMARY = "advertSummary";
    
    private static final String SEO_URL_PREFIX = "immobilien/";
    private static final String BASE_URL = "https://www.willhaben.at/iad/";
    
    private final MultipleListings multipleListings;
    
    /**
     * Initializes the fetcher with a URL and a MultipleListings instance.
     *
     * @param url             The URL to fetch listings from.
     * @param multipleListings An instance of MultipleListings to store the processed listings.
     */
    public ListingsOverviewFetcher(String url, MultipleListings multipleListings) {
        super(url);
        this.multipleListings = multipleListings;
    }
    
    /**
     * Fetches and processes listings from the URL.
     */
    public void fetchAllListings() {
        log.info("Fetching content from {}", getUrl());
        
        try {
            JsonNode parsedData = fetchContentAsJson();
            
            // Validate and extract listings
            JsonNode listingsSummary = extractListingsSummary(parsedData);
            if (listingsSummary == null || !listingsSummary.isArray() || listingsSummary.isEmpty()) {
                log.error("No listing summaries found in the JSON data.");
                return;
            }
            
            // Process each listing
            for (JsonNode singleListingBeforeConversion : listingsSummary) {
                processSingleListing(singleListingBeforeConversion);
            }
            
            log.info("Successfully fetched and processed {} listings.", listingsSummary.size());
            
        } catch (HttpTimeoutException timeoutEx) {
            log.error("HTTP timeout occurred while fetching listings: {}", timeoutEx.getMessage());
        } catch (IOException ioEx) {
            log.error("IO error occurred while fetching listings: {}", ioEx.getMessage(), ioEx);
        } catch (Exception e) {
            log.error("An unexpected error occurred: {}", e.getMessage(), e);
        }
    }
    
    /**
     * Extracts listing summaries from the parsed JSON data.
     *
     * @param parsedData The parsed JSON data.
     * @return A JsonNode containing listing summaries, or null if extraction fails.
     */
    private static JsonNode extractListingsSummary(JsonNode parsedData) {
        try {
            JsonNode props = parsedData.get(KEY_PROPS);
            if (props == null) {
                log.error("Missing '{}' key in JSON data.", KEY_PROPS);
                return null;
            }
            
            JsonNode pageProps = props.get(KEY_PAGE_PROPS);
            if (pageProps == null) {
                log.error("Missing '{}' key in JSON data.", KEY_PAGE_PROPS);
                return null;
            }
            
            JsonNode searchResult = pageProps.get(KEY_SEARCH_RESULT);
            if (searchResult == null) {
                log.error("Missing '{}' key in JSON data.", KEY_SEARCH_RESULT);
                return null;
            }
            
            JsonNode listingSummaryList = searchResult.get(KEY_LISTING_SUMMARY_LIST);
            if (listingSummaryList == null) {
                log.error("Missing '{}' key in JSON data.", KEY_LISTING_SUMMARY_LIST);
                return null;
            }
            
            JsonNode listingSummary = listingSummaryList.get(KEY_LISTING_SUMMARY);
            if (listingSummary == null) {
                log.error("Missing '{}' key in JSON data.", KEY_LISTING_SUMMARY);
                return null;
            }
            
            return listingSummary;
            
        } catch (Exception e) {
            log.error("Failed to extract listing summaries due to error: {}", e.getMessage(), e);
            return null;
        }
    }
    
    /**
     * Processes a single listing and appends it to the multiple listings.
     *
     * @param singleListingBeforeConversion The raw listing data before conversion.
     */
    private void processSingleListing(JsonNode singleListingBeforeConversion) {
        try {
            SingleListing singleListing = new SingleListing();
            
            // Navigate to the SEO URL path: attributes.attribute[19].values[0]
            JsonNode attributes = singleListingBeforeConversion.get("attributes");
            if (attributes == null) {
                log.warn("Missing 'attributes' in listing data.");
                return;
            }
            
            JsonNode attributeArray = attributes.get("attribute");
            if (attributeArray == null || !attributeArray.isArray() || attributeArray.size() <= 19) {
                log.warn("Missing or insufficient 'attribute' array in listing data.");
                return;
            }
            
            JsonNode attribute19 = attributeArray.get(19);
            if (attribute19 == null) {
                log.warn("Missing attribute at index 19 in listing data.");
                return;
            }
            
            JsonNode values = attribute19.get("values");
            if (values == null || !values.isArray() || values.isEmpty()) {
                log.warn("Missing or empty 'values' array in attribute 19.");
                return;
            }
            
            JsonNode seoUrlNode = values.get(0);
            if (seoUrlNode == null || !seoUrlNode.isTextual()) {
                log.warn("Missing or invalid SEO URL in attribute 19 values.");
                return;
            }
            
            String seoUrl = seoUrlNode.asText();
            
            if (seoUrl.startsWith(SEO_URL_PREFIX)) {
                String url = BASE_URL + seoUrl;
                singleListing.addKeyValuePair("url", url);
                multipleListings.appendListing(singleListing);
                log.debug("Added listing with URL: {}", url);
            } else {
                log.debug("Skipping listing with SEO URL that doesn't start with '{}': {}", SEO_URL_PREFIX, seoUrl);
            }
            
        } catch (Exception e) {
            log.error("Error processing single listing: {}", e.getMessage(), e);
        }
    }
} 