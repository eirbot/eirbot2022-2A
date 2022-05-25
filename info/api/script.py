#! /usr/bin/env python3
import requests

# post sur /initialize device id {"device_id":"4"}

# Vérifier 200

# get sur /find

# verifier 200 + liste

# requests.post

# requests.get

response = requests.post('http://10.42.0.158:5000/api/initialize', json={"device_id": "0"})
if response.status_code == 200:
    response = requests.get('http://10.42.0.158:5000/api/position')
    if response.status_code == 200:
        print(response.json())
    else:
        print("Erreur")
else:
    print(response.status_code)