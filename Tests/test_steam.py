import sys
import os
import re

# Add the directory containing files to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from steam import steam

def test_steam_get_game_id():
    s = steam("Baldur's Gate 3")
    assert s.get_game_id() == 1086940
    
def test_steam_get_game_info():
    s = steam("Baldur's Gate 3")
    assert isinstance(s.get_game_info(), str)
    
def test_steam_get_game_price():
    s = steam("Baldur's Gate 3")
    assert isinstance(s.get_game_price(("ukraine", re.compile(r"[0-9]+₴"))), float)