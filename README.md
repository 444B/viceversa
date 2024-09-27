# Vice Versa (Client-Server Model Exploration)
This project demonstrates a simple client-server model using Python.

## Components
- `server.py`: A server that listens on port 8080, receives UUID and timestamp data from clients, stores it in an SQLite3 database, and prints the data to the console.
- `client.py`: A client that sends a UUID and timestamp to the server every 2 seconds.

## Setup Instructions
1. Server Setup:
Ensure Python 3 is installed.

Run the server script:
```bash
chmod +x server.py; python3 server.py
```
---
2. Client Setup:
Install the requests library:
```bash
pip install requests
```
Update the SERVER_URL in client.py with your server's IP address (e.g., 'http://127.0.0.1:8080/').

Run the client script:
```bash
chmod +x client.py; python3 client.py
```