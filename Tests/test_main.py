import sys
import os

# Add the directory containing files to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import get_best_price

def test_main_get_best_price():
    res = get_best_price("Baldur's Gate 3")
    assert isinstance(res["country"], str)
    assert isinstance(res["price"], float)
    assert isinstance(res["pln_price"], float)