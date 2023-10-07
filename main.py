import re
import sys

from steam import steam
from websites import eneba

countries = [("ukraine", re.compile(r"[0-9]+₴")), ("turkey", re.compile(r"₺[0-9]+,[0-9]+")), 
             ("argentina", re.compile(r"ARS\$ [0-9]+,[0-9]+")), ("poland", re.compile(r"[0-9]+,[0-9]+zł"))]

def get_best_price(game_title: str) -> dict:
    website = eneba(countries)
    game = steam(game_title)
    
    result = {
        "country": None,
        "price": None,
        "pln_price": None
    }
    
    # Exchange rate format currency / pln [amount of currency per 1 pln]
    for country in countries:
        website.set_region(country)
        exchange_rate = website.get_price()
        
        game_price = game.get_game_price(country)
        pln_price = game_price / exchange_rate
        
        if result["pln_price"] is None or pln_price < result["pln_price"]:
            result["country"] = country[0]
            result["price"] = game_price
            result["pln_price"] = pln_price
            
    return result
        
        
        
if __name__ == "__main__":
    res = get_best_price(sys.argv[1])
    print(res)