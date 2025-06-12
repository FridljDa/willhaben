package de.danielfridljand.willhaben.listing.fetcher;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.Duration;
import java.util.regex.Pattern;

@Slf4j
public class Fetcher {
    
    private static final String NEXT_DATA_START = "<script id=\"__NEXT_DATA__\" type=\"application/json\">";
    private static final String NEXT_DATA_END = "</script>";
    private static final Pattern ROWS_PATTERN = Pattern.compile("&rows=\\d+&");
    
    private final String url;
    private final boolean isUrl;
    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;
    
    public Fetcher(String url) {
        this.isUrl = !isFilePath(url);
        
        if (this.isUrl) {
            // Replace rows parameter to get more results (like in Python version)
            this.url = ROWS_PATTERN.matcher(url).replaceAll("&rows=1000&");
        } else {
            this.url = url;
        }
        
        this.httpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(30))
                .build();
        this.objectMapper = new ObjectMapper();
    }
    
    /**
     * Fetches the HTML content from a URL or local file path and extracts JSON data.
     *
     * @return The extracted JSON data as a JsonNode.
     * @throws IOException if there's an error fetching or processing the content.
     */
    public JsonNode fetchContentAsJson() throws IOException {
        String htmlContent;
        
        if (isUrl) {
            htmlContent = fetchHtml();
        } else {
            // It's a local file path
            Path filePath = Paths.get(url);
            htmlContent = Files.readString(filePath);
        }
        
        return extractJsonFromHtml(htmlContent);
    }
    
    /**
     * Fetches HTML content from the URL.
     *
     * @return The HTML content as a string.
     * @throws IOException if there's an error making the HTTP request.
     */
    private String fetchHtml() throws IOException {
        try {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .timeout(Duration.ofSeconds(30))
                    .GET()
                    .build();
            
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            
            if (response.statusCode() != 200) {
                throw new IOException("HTTP request failed with status code: " + response.statusCode());
            }
            
            return response.body();
            
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IOException("HTTP request was interrupted", e);
        }
    }
    
    /**
     * Extracts JSON data embedded in the HTML content.
     *
     * @param htmlContent The HTML content as a string.
     * @return The extracted JSON data as a JsonNode.
     * @throws IOException if JSON parsing fails.
     */
    public JsonNode extractJsonFromHtml(String htmlContent) throws IOException {
        try {
            int startIndex = htmlContent.indexOf(NEXT_DATA_START);
            if (startIndex == -1) {
                log.error("Failed to locate JSON data start marker in the HTML content.");
                return objectMapper.createObjectNode(); // Return empty JSON object
            }
            
            startIndex += NEXT_DATA_START.length();
            int endIndex = htmlContent.indexOf(NEXT_DATA_END, startIndex);
            
            if (endIndex == -1) {
                log.error("Failed to locate JSON data end marker in the HTML content.");
                return objectMapper.createObjectNode(); // Return empty JSON object
            }
            
            String jsonData = htmlContent.substring(startIndex, endIndex);
            return objectMapper.readTree(jsonData);
            
        } catch (Exception e) {
            log.error("Failed to extract and parse JSON data from HTML content", e);
            return objectMapper.createObjectNode(); // Return empty JSON object
        }
    }
    
    /**
     * Determines if the given string is a file path or URL.
     *
     * @param input The input string to check.
     * @return true if it's a file path, false if it's a URL.
     */
    private boolean isFilePath(String input) {
        // Simple heuristic: if it starts with http/https, it's a URL
        return !input.toLowerCase().startsWith("http://") && !input.toLowerCase().startsWith("https://");
    }
    
    public String getUrl() {
        return url;
    }
    
    public boolean isUrl() {
        return isUrl;
    }
}
