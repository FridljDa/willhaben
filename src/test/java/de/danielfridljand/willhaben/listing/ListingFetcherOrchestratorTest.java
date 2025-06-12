package de.danielfridljand.willhaben.listing;

import de.danielfridljand.willhaben.listing.structure.SingleListing;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.BeforeEach;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.*;

class ListingFetcherOrchestratorTest {

    private static final Logger logger = LoggerFactory.getLogger(ListingFetcherOrchestratorTest.class);
    
    private static final String TEST_URL_QUERY = "https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sort=1&rows=1000&isNavigation=true&sfId=7c07d0eb-68b5-46e8-8e40-e47a743a85b0&ESTATE_PREFERENCE=28&areaId=117223&areaId=117224&areaId=117225&areaId=117226&areaId=117227&areaId=117228&areaId=117229&areaId=117230&areaId=117231&page=1&PRICE_FROM=0&PRICE_TO=1100&ESTATE_SIZE/LIVING_AREA_FROM=40";
    
    private ListingFetcherOrchestrator orchestrator;
    private Path testOutputPath;

    @BeforeEach
    void setUp() {
        // Create a temporary path for test output
        testOutputPath = Paths.get("target", "test-output", "listings-test.json");
        
        // Create orchestrator in non-silent mode for better test visibility
        orchestrator = new ListingFetcherOrchestrator(TEST_URL_QUERY, testOutputPath, false);
        
        logger.info("Test setup completed. Output path: {}", testOutputPath);
    }

    @Test
    @DisplayName("Should successfully fetch and process listings from willhaben.at")
    @Timeout(value = 5, unit = TimeUnit.MINUTES) // 5 minute timeout for network operations
    void testFetchAndProcessListings() {
        logger.info("Starting integration test for fetchAndProcessListings");
        logger.info("URL: {}", TEST_URL_QUERY);
        
        // Execute the main method under test
        assertDoesNotThrow(() -> {
            orchestrator.fetchAndProcessListings();
        }, "fetchAndProcessListings should not throw any exceptions");
        
        // Verify that listings were actually fetched
        assertNotNull(orchestrator.getMultipleListings(), "MultipleListings should not be null");
        assertTrue(orchestrator.getMultipleListings().size() > 0, 
                  "Should have fetched at least one listing");
        
        logger.info("Fetched {} listings", orchestrator.getMultipleListings().size());
        
        // Verify that each listing has basic properties
        for (int i = 0; i < Math.min(5, orchestrator.getMultipleListings().size()); i++) {
            SingleListing listing = orchestrator.getMultipleListings().getListing(i);
            
            assertNotNull(listing, "Listing should not be null");
            assertNotNull(listing.getProperties(), "Listing properties should not be null");
            assertFalse(listing.getProperties().isEmpty(), "Listing should have at least one property");
            
            // Every listing should have a URL (this is set in the overview fetcher)
            assertTrue(listing.hasProperty("url"), 
                      String.format("Listing %d should have a URL property", i));
            
            Object url = listing.getProperty("url");
            assertNotNull(url, "URL should not be null");
            assertTrue(url.toString().startsWith("https://www.willhaben.at/iad/"), 
                      "URL should be a valid willhaben URL");
            
            logger.info("Listing {}: URL = {}, Properties = {}", 
                       i + 1, url, listing.getProperties().size());
        }
        
        logger.info("Integration test completed successfully");
    }
    
    @Test
    @DisplayName("Should handle silent mode correctly")
    @Timeout(value = 3, unit = TimeUnit.MINUTES)
    void testFetchAndProcessListingsInSilentMode() {
        logger.info("Testing silent mode functionality");
        
        // Create orchestrator in silent mode
        ListingFetcherOrchestrator silentOrchestrator = 
            new ListingFetcherOrchestrator(TEST_URL_QUERY, null, true);
        
        // Should not throw exceptions even in silent mode
        assertDoesNotThrow(() -> {
            silentOrchestrator.fetchAndProcessListings();
        }, "fetchAndProcessListings should work in silent mode");
        
        // Should still fetch listings
        assertTrue(silentOrchestrator.getMultipleListings().size() > 0, 
                  "Should fetch listings even in silent mode");
        
        logger.info("Silent mode test completed. Fetched {} listings", 
                   silentOrchestrator.getMultipleListings().size());
    }
    
    @Test
    @DisplayName("Should create orchestrator with correct parameters")
    void testOrchestratorInitialization() {
        // Test the orchestrator was initialized correctly
        assertEquals(TEST_URL_QUERY, orchestrator.getUrlQuery(), 
                    "URL query should match the provided value");
        assertEquals(testOutputPath, orchestrator.getMultipleListings().getPath(), 
                    "Path should match the provided value");
        assertFalse(orchestrator.isSilent(), 
                   "Silent mode should be false for this test setup");
        
        logger.info("Orchestrator initialization test completed");
    }
    
    @Test
    @DisplayName("Should handle network issues gracefully")
    void testNetworkErrorHandling() {
        logger.info("Testing network error handling with invalid URL");
        
        // Test with an invalid URL to simulate network issues
        String invalidUrl = "https://invalid-domain-that-does-not-exist.com/test";
        ListingFetcherOrchestrator invalidOrchestrator = 
            new ListingFetcherOrchestrator(invalidUrl, null, true);
        
        // Should throw a RuntimeException (as per the implementation)
        RuntimeException exception = assertThrows(RuntimeException.class, () -> {
            invalidOrchestrator.fetchAndProcessListings();
        }, "Should throw RuntimeException for network errors");
        
        assertTrue(exception.getMessage().contains("Failed to fetch and process listings"), 
                  "Exception message should indicate the failure reason");
        
        logger.info("Network error handling test completed. Exception: {}", exception.getMessage());
    }
} 