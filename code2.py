import requests
import sys

def check_server_header(url, host_header):
    headers = {
        'Host': host_header,
        'Connection': 'close'
    }
    
    try:
        response = requests.get(url, headers=headers)
        server_header = response.headers.get('Server', '')
        
        if 'AkamaiGHost' in server_header or 'cloudflare' in server_header:
            print(f"Invalid server header for URL {url}: {server_header}")
        else:
            print(f"Valid response for URL {url}:\n{response.text}")
    except requests.RequestException as e:
        print(f"Request to {url} failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]

    try:
        with open(filename, 'r') as file:
            urls = file.readlines()
        
        for url in urls:
            url = url.strip()
            if url:
                check_server_header(url, 'xyz.com')
    except FileNotFoundError:
        print(f"File {filename} not found.")
        sys.exit(1)
