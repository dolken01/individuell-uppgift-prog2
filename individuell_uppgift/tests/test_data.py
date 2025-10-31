import pytest
import flask
import ssl
import urllib
import requests

context = ssl._create_unverified_context()

def test_Is_online_index(): # Testar om startsidan är online
    assert urllib.request.urlopen("http://127.0.0.1:5000", context=context, timeout=10)

def test_404_response(): 
    response = requests.get("http://127.0.0.1:5000/abc")
    assert response.status_code == 404






