#!/usr/bin/env python3
import argparse
import logging
import os
import sys
import uuid
import time
import requests

# Set up command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Client Script')
    parser.add_argument('--dst_ip', type=str, default='10.132.0.3', help='Destination IP/Domain')
    parser.add_argument('--port', type=int, default=80, help='Destination Port')
    parser.add_argument('--logging', type=str, default='info', help='Logging level (debug, info, warning, error)')
    return parser.parse_args()

# Set up logging
def setup_logging(log_level):
    log_levels = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING, 'error': logging.ERROR}
    log_level = log_levels.get(log_level.lower(), logging.INFO)
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    timestamp = time.strftime('%Y%m%d-%H%M%S')
    log_filename = os.path.join(log_dir, f'client_{timestamp}.log')
    logging.basicConfig(filename=log_filename, level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

# Main function to send data
def send_data(dst_ip, port):
    try:
        data = {
            'timestamp': int(time.time()),
            'uuid': str(uuid.uuid4()),
            'optional_info': 'Sample Data'
        }
        url = f'http://{dst_ip}:{port}/data'
        response = requests.post(url, json=data)
        response.raise_for_status()
        logging.info(f'Successfully sent data to {url}')
    except Exception as e:
        logging.error(f'Failed to send data: {e}')
        sys.exit(1)

if __name__ == '__main__':
    args = parse_arguments()
    setup_logging(args.logging)
    send_data(args.dst_ip, args.port)
