import requests
import random
import argparse
from urllib.parse import urljoin

def generate_random_value():
    return random.randint(10000, 99999)

def send_requests(base_url, random_value, proxy):
    proxies = {
        "http": proxy,
        "https": proxy
    }
    for _ in range(10):
        url = urljoin(base_url, f"?k={random_value}")
        response = requests.get(url, proxies=proxies)
        print(f"Request to {url} returned status code {response.status_code}")

def check_response(base_url, random_value, proxy):
    proxies = {
        "http": proxy,
        "https": proxy
    }
    check_url = urljoin(base_url, f"?k={random_value}")
    response = requests.get(check_url, proxies=proxies)
    if response.status_code == 200 and response.text.strip() == "{}":
        print(f"The URL {check_url} is valid and returned an empty JSON object.")
    else:
        print(f"The URL {check_url} is not valid or did not return an empty JSON object.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send requests and check response.")
    parser.add_argument("base_url", help="The base URL to send requests to.")
    parser.add_argument("--proxy", default=None, help="Proxy server to use for the requests (e.g., http://proxy.example.com:8080)")

    args = parser.parse_args()

    random_value = generate_random_value()
    send_requests(args.base_url, random_value, args.proxy)
    check_response(args.base_url, random_value, args.proxy)
