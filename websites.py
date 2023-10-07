import undetected_chromedriver as uc
import json
import bs4
import re
from currency_converter import CurrencyConverter

# Website class to share region across websites
class website:
    def __init__(self, region):
        self.region = region
             
class eneba(website):
    def __init__(self, countries):
        # Default region is the first one in the list
        super().__init__(countries[0])
            
        self.url = r"https://www.eneba.com/us/store/steam-gift-cards?"
        self.params = {
            "drms[]": "steam gift card",
            "page": 1,
            "regions[]": self.region,
            "types[]": "giftcard"
        }
        
        # Generate url
        for param in self.params:
            self.url += f"{param}={self.params[param]}&"
        
    def set_region(self, region):
        self.__init__(region)
        
    def get_data(self) -> dict | None:
        driver = uc.Chrome()
        
        # Load website
        driver.minimize_window()
        driver.get(self.url)
        
        # Get the page source
        response = driver.page_source
        driver.close()
        
        soup = bs4.BeautifulSoup(response, "html.parser")
        
        # Find script with json data
        script_elements = soup.find_all("script")
        script = max(script_elements, key=lambda s: len(s.text))
        # Load json
        data = json.loads(script.text)
        return data
        
    def get_auctions(self) -> tuple | None:
        data = self.get_data()
        
        # Find products
        for key in data:
            if "Product" in key:
                product = data[key]
                name = product.get("name")
                auction_id = product.get("cheapestAuction")
                return (auction_id, name, data)
        return None
                
    def get_price(self) -> float | None:
        auction_id, name, data = self.get_auctions()
        
        # Check if auction id is valid
        if not auction_id:
            return
        
        # Get auction id
        auction_id = auction_id["__ref"]
        auction = data[auction_id]
        
        # Find key for price data
        search_term = "price"
        key = [k for k in auction if search_term in k][0]
        
        # Check the price
        price_data = auction[key]
        price = float(price_data["amount"]) / 100
        
        # Check the currency amount
        amount = int(re.findall("[0-9]+", name)[0])
        
        # Convert euro to pln
        price = CurrencyConverter().convert(price, 'EUR', 'PLN')
        
        # Calculate currency amount per PLN
        amount_per_pln = amount / price
        
        return amount_per_pln      
