# Willhaben API
This module has only tested on `https://willhaben.at`!

## Documentation
There are two ways you can use this API.
Either by entering the URL and let the API extract all the results or by using the builder to build the URL and let the API extract the results.


#### Extract results directly from URL
For this method you need an URL of the willhaben search you want to make. Then you use the .getListings(URL) function and it returns a promise which resolves to an array with all the results.

###### Example
This example searches for `rtx` in the `Grafikkarten` category and will show the first 1000 results.
```python
url = "https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sort=1&rows=30"
listings = get_listings(url)
print(listings)
```