import sys
import os
import re

# Add the directory containing files to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from websites import eneba

def test_eneba_get_data():
    e = eneba([("ukraine", re.compile(r"[0-9]+₴"))])
    assert isinstance(e.get_data(), dict)
    
def test_eneba_get_auctions():
    e = eneba([("ukraine", re.compile(r"[0-9]+₴"))])
    assert isinstance(e.get_auctions(), tuple)
    
def test_eneba_get_price():
    e = eneba([("ukraine", re.compile(r"[0-9]+₴"))])
    assert isinstance(e.get_price(), float)