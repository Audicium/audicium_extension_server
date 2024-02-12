import json

import requests


# url = 'www.google.com'


def home_page(url: str) -> json:
    response = requests.get(url)
    return {'text': 'from google'}
