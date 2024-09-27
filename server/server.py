#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3
import json
import sys

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the length of the data
        content_length = int(self.headers['Content-Length'])
        # Read the data
        post_data = self.rfile.read(content_length)
        # Parse JSON data
        try:
            data = json.loads(post_data)
            uuid_value = data['uuid']
            timestamp = data['timestamp']
        except (json.JSONDecodeError, KeyError) as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid data")
            return

        # Write to database
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS data (uuid TEXT, timestamp INTEGER)')
        c.execute('INSERT INTO data (uuid, timestamp) VALUES (?, ?)', (uuid_value, timestamp))
        conn.commit()
        conn.close()

        # Print to stdout
        print(f"Received UUID: {uuid_value}, Timestamp: {timestamp}")

        # Send response
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Data received")

def run(server_class=HTTPServer, handler_class=MyHandler):
    server_address = ('', 8080)  # Changed port to 8080
    httpd = server_class(server_address, handler_class)
    print('Starting HTTP server on port 8080...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down the server.')
        httpd.server_close()

if __name__ == '__main__':
    run()