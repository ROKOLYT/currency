import requests
import json
import bs4
import undetected_chromedriver as uc
import re


class steam():
    def __init__(self, game: str):
        self.game = game.lower()
        self.game_id = self.get_game_id()
        
        self.soup = None
    
    def get_game_id(self) -> int | None:
        response = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/")
        
        if response.status_code == 200:
            app_list = response.json()["applist"]["apps"]

            # Find the game in the list
            game_id = next((app["appid"] for app in app_list if app["name"].lower() == self.game), None)
            
            return game_id
        else:
            return None
        
    def get_game_info(self) -> str:
        options = uc.ChromeOptions()
        options.headless = False
        driver = uc.Chrome(options=options)
        
        # Load website
        driver.minimize_window()
        driver.get(f"https://steamdb.info/app/{self.game_id}/")
        
        # Get the page source
        response = driver.page_source
        driver.close()
        
        return response
    
    def get_game_price(self, country: tuple) -> float:
        if self.soup is None:
            self.soup = bs4.BeautifulSoup(self.get_game_info(), "html.parser")
        
        # Find the price
        price = self.soup.find("td", string=country[1]).text
        
        # Remove the currency symbol
        price = re.sub(r'[^0-9,]', '', price)
        
        # Replace , with .
        price = price.replace(',', '.')
    
        return float(price)
