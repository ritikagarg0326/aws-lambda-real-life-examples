import requests

def send_to_lambda(data, lambda_url):
    requests.post(lambda_url, json=data)