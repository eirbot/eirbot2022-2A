#! /usr/bin/env python3
"""
Example with get request
"""
import requests

response = requests.get('http://localhost:5000/')
print(response.text)

response = requests.get('http://localhost:5000/int')
print(int(response.text))
