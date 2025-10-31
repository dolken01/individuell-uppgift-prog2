import pytest
import flask
import ssl
import urllib
import requests

context = ssl._create_unverified_context()

def test_Is_online_index():
    """ Testar om huvud sidan är online """
    assert urllib.request.urlopen("http://127.0.0.1:5000", context=context, timeout=10)



def test_404_response(): 
    """ Testar 404 felhantering """
    response = requests.get("http://127.0.0.1:5000/abc")
    assert response.status_code == 404

def test_invalid_date(): 
    """ Testar ogiltigt datumformat """
    response = requests.post("http://127.0.0.1:5000/priser", data={
        "year": "2024",
        "month": "aa", 
        "day": "10",
        "area": "SE3"
    })
    assert response.status_code == 400
    assert "Ogiltigt datumformat" in response.text

def test_valid_date():
    """ Testar giltigt datumformat """
    response = requests.post("http://127.0.0.1:5000/priser", data={
        "year": "2025",
        "month": "10",
        "day": "30",
        "area": "SE3"
    })
    assert response.status_code == 200
    assert "SEK_per_kWh" in response.text

def test_too_low_date():
    """ Testar datum för långt bak """
    response = requests.post("http://127.0.0.1:5000/priser", data={
        "year": "2021",
        "month": "10",
        "day": "10",
        "area": "SE3"
    })
    assert response.status_code == 400
    assert "datum för långt bak." in response.text








