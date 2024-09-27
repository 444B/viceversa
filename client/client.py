#!/usr/bin/env python3
import requests
import uuid
import time

# Replace 'server_ip_address' with the actual server IP or hostname
SERVER_URL = 'http://10.132.0.4:8080/'  # Ensure this is correct

def main():
    # Generate a persistent UUID for this client instance
    client_uuid = str(uuid.uuid4())
    print(f"Client UUID: {client_uuid}")

    while True:
        # Generate data
        data = {
            'uuid': client_uuid,
            'timestamp': int(time.time())
        }

        try:
            response = requests.post(SERVER_URL, json=data)
            print(f"Sent data: {data}, Server response: {response.text}")
        except requests.exceptions.RequestException as e:
            print('Request failed:', e)
        
        # Wait for 2 seconds before sending the next request
        time.sleep(2)

if __name__ == '__main__':
    main()