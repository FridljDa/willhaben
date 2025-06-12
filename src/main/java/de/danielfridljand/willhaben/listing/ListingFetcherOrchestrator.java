package de.danielfridljand.willhaben.listing;

import de.danielfridljand.willhaben.listing.fetcher.ListingDetailsFetcher;
import de.danielfridljand.willhaben.listing.fetcher.ListingsOverviewFetcher;
import de.danielfridljand.willhaben.listing.structure.MultipleListings;
import de.danielfridljand.willhaben.listing.structure.SingleListing;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;

import java.nio.file.Path;

@Data
@Slf4j
public class ListingFetcherOrchestrator {
    
    private final String urlQuery;
    private final MultipleListings multipleListings;
    private final boolean silent;
    
    /**
     * Constructor with URL query, optional path, and silent flag.
     *
     * @param urlQuery The URL query string for fetching listings
     * @param path     Optional path for storing/loading listings (can be null)
     * @param silent   Whether to operate in silent mode (default: true)
     */
    public ListingFetcherOrchestrator(String urlQuery, Path path, boolean silent) {
        this.urlQuery = urlQuery;
        this.multipleListings = new MultipleListings(path);
        this.silent = silent;
    }
    
    /**
     * Constructor with URL query and optional path, defaulting to silent mode.
     *
     * @param urlQuery The URL query string for fetching listings
     * @param path     Optional path for storing/loading listings (can be null)
     */
    public ListingFetcherOrchestrator(String urlQuery, Path path) {
        this(urlQuery, path, true);
    }
    
    /**
     * Constructor with URL query only, defaulting to no path and silent mode.
     *
     * @param urlQuery The URL query string for fetching listings
     */
    public ListingFetcherOrchestrator(String urlQuery) {
        this(urlQuery, null, true);
    }
    
    /**
     * Fetches and processes all listings from the configured URL.
     * This method orchestrates the entire workflow:
     * 1. Fetches listing overview/summaries
     * 2. Fetches detailed information for each listing
     * 3. Optionally displays results if not in silent mode
     */
    public void fetchAndProcessListings() {
        log.info("Starting listing fetch and process workflow for URL: {}", urlQuery);
        
        try {
            // Step 1: Fetch all listing overviews
            log.info("Fetching listing overviews...");
            ListingsOverviewFetcher overviewFetcher = new ListingsOverviewFetcher(urlQuery, multipleListings);
            overviewFetcher.fetchAllListings();
            
            int overviewCount = multipleListings.size();
            log.info("Fetched {} listing overviews", overviewCount);
            
            if (overviewCount == 0) {
                log.warn("No listings found in overview. Workflow completed.");
                if (!silent) {
                    System.out.println("No listings found.");
                }
                return;
            }
            
            // Step 2: Fetch detailed information for each listing
            log.info("Fetching detailed information for each listing...");
            applyDetailsFetcherToEachListing();
            
            // Step 3: Display results if not in silent mode
            if (!silent) {
                multipleListings.prettyPrint();
                System.out.printf("Number of listings: %d%n", multipleListings.size());
            }
            
            log.info("Listing fetch and process workflow completed successfully. Total listings: {}", multipleListings.size());
            
        } catch (Exception e) {
            log.error("Error during listing fetch and process workflow: {}", e.getMessage(), e);
            if (!silent) {
                System.err.printf("Error processing listings: %s%n", e.getMessage());
            }
            throw new RuntimeException("Failed to fetch and process listings", e);
        }
    }
    
    /**
     * Applies the ListingDetailsFetcher to each listing in the collection.
     * This is equivalent to the Python lambda function approach.
     */
    private void applyDetailsFetcherToEachListing() {
        int totalListings = multipleListings.size();
        int processedCount = 0;
        int errorCount = 0;
        
        for (SingleListing singleListing : multipleListings.getAllListings()) {
            try {
                processedCount++;
                if (!silent && processedCount % 10 == 0) {
                    log.info("Processing listing {} of {}", processedCount, totalListings);
                }
                
                ListingDetailsFetcher detailsFetcher = new ListingDetailsFetcher(singleListing);
                detailsFetcher.fetchAndSetSingleListingContent();
                
            } catch (Exception e) {
                errorCount++;
                log.error("Failed to fetch details for listing {}: {}", processedCount, e.getMessage());
                
                // Continue processing other listings even if one fails
                if (!silent) {
                    System.err.printf("Warning: Failed to fetch details for listing %d: %s%n", 
                                    processedCount, e.getMessage());
                }
            }
        }
        
        log.info("Completed detail fetching: {} processed, {} errors", processedCount, errorCount);
        
        if (errorCount > 0 && !silent) {
            System.out.printf("Warning: %d listings had errors during detail fetching%n", errorCount);
        }
    }
}
