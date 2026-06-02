import requests

BACKEND_URL = "http://backend:8000/"


def make_get_request(endpoint: str) -> object:
    res = requests.get(f"{BACKEND_URL}{endpoint}")
    if res.status_code == 200:
        return res.json()
