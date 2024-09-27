#!/usr/bin/env python3
import argparse
import logging
import os
import sys
import time
import sqlite3
from flask import Flask, request, jsonify
import threading

# Set up command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Server Script')
    parser.add_argument('--port', type=str, default='80', help='Comma-separated list of ports to listen on')
    parser.add_argument('--db', type=str, default='db/main_sql.db', help='Database file path')
    parser.add_argument('--run_streamlit', type=str, default='false', help='Run Streamlit app (true/false)')
    parser.add_argument('--logging', type=str, default='info', help='Logging level (debug, info, warning, error)')
    return parser.parse_args()

# Set up logging
def setup_logging(log_level):
    log_levels = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING, 'error': logging.ERROR}
    log_level = log_levels.get(log_level.lower(), logging.INFO)
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    timestamp = time.strftime('%Y%m%d-%H%M%S')
    log_filename = os.path.join(log_dir, f'server_{timestamp}.log')
    logging.basicConfig(filename=log_filename, level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the database
def init_db(db_path):
    db_dir = os.path.dirname(db_path)
    os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            uuid TEXT,
            optional_info TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Flask app to receive data
def create_app(db_path):
    app = Flask(__name__)

    @app.route('/data', methods=['POST'])
    def receive_data():
        try:
            content = request.json
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO data (timestamp, uuid, optional_info)
                VALUES (?, ?, ?)
            ''', (content['timestamp'], content['uuid'], content.get('optional_info', '')))
            conn.commit()
            conn.close()
            logging.info(f"Received data: {content}")
            return jsonify({'status': 'success'}), 200
        except Exception as e:
            logging.error(f'Error receiving data: {e}')
            return jsonify({'status': 'error', 'message': str(e)}), 500

    return app

# Run the server on multiple ports if needed
def run_server(app, ports):
    for port in ports:
        threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(port), debug=False, use_reloader=False)).start()
        logging.info(f'Server is running on port {port}')

# Optional Streamlit app
def run_streamlit_app():
    os.system('streamlit run streamlit_app.py')

if __name__ == '__main__':
    args = parse_arguments()
    setup_logging(args.logging)
    init_db(args.db)
    app = create_app(args.db)
    port_list = args.port.split(',')
    run_server(app, port_list)
    if args.run_streamlit.lower() == 'true':
        run_streamlit_app()
