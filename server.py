import socket
import threading
import time
from base64 import b64decode
from bitarray import bitarray

import helper
from helper import *

from datetime import datetime

cbf_storage = {}
cbf_expire_time = helper.dbf_life_cycle


def timestamp_to_date(timestamp=None):
    if timestamp is None:
        timestamp = time.time()
    date_time = datetime.fromtimestamp(timestamp)
    formatted_date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date_time


# change to
def recover(bf_b64encoded):
    bf_bytes = b64decode(bf_b64encoded)
    bf = bitarray()
    bf.frombytes(bf_bytes)

    indices = [i for i, bit in enumerate(bf) if bit]

    return indices


def server_loop():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((helper.BACKEND_SERVER_IP, helper.BACKEND_SERVER_PORT))
    server.listen(5)
    print_colored(f"[*] Listening on {helper.BACKEND_SERVER_IP}:{helper.BACKEND_SERVER_PORT}")

    while True:
        client_socket, _ = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


def handle_client(client_socket):
    try:
        data = client_socket.recv(1024).decode('utf-8')
        bf_type, bf_b64encoded = data.split("|")
        bf_data = recover(bf_b64encoded)

        if bf_type == 'qbf':
            clear_cbf()
            matched = check_by_qbf(bf_data)
            result = 'you are at risk' if matched else 'you are safe'
        elif bf_type == 'cbf':
            upload_cbf(bf_data)
            result = 'uploaded cbf successfully'
        # elif bf_type == 'attacker':
        #     upload_cbf(bf_data)
        #     result = 'attacker made fake message successfully'
        else:
            result = 'invalid type'
        client_socket.send(result.encode())
    finally:
        client_socket.close()


def upload_cbf(cbf):
    store_time = time.time()
    cbf_storage[store_time] = cbf
    formatted_cbf = {timestamp_to_date(k): v for k, v in cbf_storage.items()}

    print_colored(f"CBF created at {timestamp_to_date(store_time)}: {cbf}\n"
                  f"CBF storage:{formatted_cbf}", 'green')


def clear_cbf():
    for store_time, cbf in list(cbf_storage.items()):
        current_time = time.time()
        if current_time - store_time >= cbf_expire_time:
            del cbf_storage[store_time]
            print_colored(
                f"[*] CBF expired at {timestamp_to_date(current_time)} which created at{timestamp_to_date(store_time)}\n"
                f"[*] Now cbf storage have keys {[timestamp_to_date(key) for key in cbf_storage.keys()]}",
                'red')


def check_by_qbf(qbf):
    formatted_cbf = {timestamp_to_date(k): v for k, v in cbf_storage.items()}

    # is_match = any(cbf in qbf for cbflist in cbf_storage.values() for cbf in cbflist)
    is_match = any(insection(cbf, qbf) for cbf in cbf_storage.values())
    print_colored(f"10-C\n"
                  f"query matched:{is_match}\n"
                  f"QBF: {qbf}\n"
                  f"CBF storage: {formatted_cbf}", 'green')
    return is_match


def insection(a, b, n=3):
    set1 = set(a)
    set2 = set(b)

    # Find common elements
    common_elements = set1.intersection(set2)

    # Check if the count of common elements is at least n
    return len(common_elements) >= n

if __name__ == "__main__":
    server_loop()
