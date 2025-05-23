import com.example.willhaben.listing.structure.Listing;
import com.example.willhaben.listing.structure.ListingRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Path;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class ListingRepositoryTest {
    private ListingRepository repository;
    private Path mockPath;

    @BeforeEach
    void setUp() {
        mockPath = Path.of("test_listings.csv");
        repository = new ListingRepository(mockPath);
    }

    @Test
    void testPrettyPrint() {
        Listing listing = new Listing();
        listing.addKeyValuePair("key1", "value1");
        repository.appendListing(listing);

        assertDoesNotThrow(() -> repository.prettyPrint());
    }

    @Test
    void testListOfListingsToDict() {
        Listing listing = new Listing();
        listing.addKeyValuePair("key1", "value1");
        repository.appendListing(listing);

        List<Map<String, Optional<String>>> result = repository.listOfListingsToDict();
        assertEquals(1, result.size());
        assertEquals(Optional.of("value1"), result.get(0).get("key1"));
    }

    @Test
    void testReadAndSetMultipleListingsFromCsvFile() throws IOException {
        // Mock CSV file content
        String csvContent = "key1,key2\nvalue1,value2\nvalue3,value4";
        Files.writeString(mockPath, csvContent);

        repository.readAndSetMultipleListingsFromCsvFile();

        List<Listing> listings = repository.getListOfListings();
        assertEquals(2, listings.size());
        assertEquals("value1", listings.get(0).getListingDict().get("key1").orElse(null));
        assertEquals("value4", listings.get(1).getListingDict().get("key2").orElse(null));
    }

    @Test
    void testWriteMultipleListingsToCsvFile() throws IOException {
        Listing listing1 = new Listing();
        listing1.addKeyValuePair("key1", "value1");
        Listing listing2 = new Listing();
        listing2.addKeyValuePair("key2", "value2");

        repository.appendListing(listing1);
        repository.appendListing(listing2);

        repository.writeMultipleListingsToCsvFile();

        String writtenContent = Files.readString(mockPath);
        assertTrue(writtenContent.contains("key1,key2"));
        assertTrue(writtenContent.contains("value1,"));
        assertTrue(writtenContent.contains(",value2"));
    }

    @Test
    void testSelectListingKeysAnd() {
        Listing listing = new Listing();
        listing.addKeyValuePair("key1", "value1");
        listing.addKeyValuePair("key2", "value2");
        repository.appendListing(listing);

        repository.selectListingKeysAnd(List.of("key1"));

        List<Listing> listings = repository.getListOfListings();
        assertEquals(1, listings.size());
        assertEquals("value1", listings.get(0).getListingDict().get("key1").orElse(null));
        assertNull(listings.get(0).getListingDict().get("key2").orElse(null));
    }

    @Test
    void testApplyFunctionToEachListing() {
        Listing listing = new Listing();
        listing.addKeyValuePair("key1", "value1");
        repository.appendListing(listing);

        repository.applyFunctionToEachListing(l -> l.addKeyValuePair("key2", "value2"));

        List<Listing> listings = repository.getListOfListings();
        assertEquals("value2", listings.get(0).getListingDict().get("key2").orElse(null));
    }

    @Test
    void testAppendListing() {
        Listing listing = new Listing();
        repository.appendListing(listing);

        assertEquals(1, repository.getListOfListings().size());
    }
}