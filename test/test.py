import unittest
from app import get_listings

class TestWillhabenAPI(unittest.TestCase):
    def test_should_return_results(self):
        url = 'https://willhaben.at/iad/kaufen-und-verkaufen/marktplatz/pc-komponenten-5878'
        listings = get_listings(url)
        self.assertNotEqual(len(listings), 0, "length of result is not 0")

if __name__ == '__main__':
    unittest.main()