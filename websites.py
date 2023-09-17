import requests
import json
import bs4
import re
from currency_converter import CurrencyConverter

countries = ["ukraine", "turkey", "argentina"]
# website class to share region across websites
class website:
    def __init__(self, region):
        self.region = region
             
class eneba(website):
    def __init__(self, region):
        super().__init__(region)
        # create currency dict if not exsists
        try:
            isinstance(self.currency, dict)
        except AttributeError:
            self.currency = {country: None for country in countries}
            
        self.url = r"https://www.eneba.com/us/store/steam-gift-cards"
        self.params = {
            "drms[]": "steam gift card",
            "page": 1,
            "regions[]": self.region,
            "types[]": "giftcard"
        }
        
    def set_region(self, region):
        self.__init__(region)
        
    def get_data(self):
        # fetch data from website
        res = requests.get(self.url, params=self.params)
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        
        # find script with json data
        script_elements = soup.find_all("script")
        script = max(script_elements, key=lambda s: len(s.text))
        # load json
        data = json.loads(script.text)
        self.get_auctions(data)
        
    def get_auctions(self, data):
        # find products
        for key in data:
            if "Product" in key:
                product = data[key]
                name = product.get("name")
                auction_id = product.get("cheapestAuction")
                self.get_price(auction_id, name, data)
                
    def get_price(self, auction_id, name, data):
        
        if not auction_id:
            return
        
        # get auction id
        auction_id = auction_id["__ref"]
        auction = data[auction_id]
        
        # find key for price data
        search_term = "price"
        key = [k for k in auction if search_term in k][0]
        
        # check the price
        price_data = auction[key]
        price = float(price_data["amount"]) / 100
        
        # check the currency amount
        amount = int(re.findall("[0-9]+", name)[0])
        
        # convert euro to pln
        price = CurrencyConverter().convert(price, 'EUR', 'PLN')
        
        # calculate currency amount per PLN
        amount_per_pln = amount / price
        
        if self.currency[self.region] is None:
            self.currency[self.region] = (amount_per_pln, name)
        else:
            amount_per_pln = max(amount_per_pln, self.currency[self.region][0])
            self.currency[self.region] = (amount_per_pln, name)        
            
                
if __name__ == "__main__":
    website = eneba("ukraine")
    for country in countries:
        website.set_region(country)
        website.get_data()
        
    print(website.currency)