import socket
import json
import socket

from bloom import *
from helper import *


broadcast_ip = '255.255.255.255'
port = 12345
n = 5
k = 3  # received >= 3 shares of the same EphID
receive_time_out = 9  # This means that if the nodes have remained in contact for at least 9 seconds
drop_rate = 0.0  # If this number is less than 0.5, don’t transmit that message
interval = 15  # seconds between new EphID generation
# bits = 2  # Generate a 32-Byte Ephemeral ID (EphID)
encid_size = 4  # 4bytes
dbf_servant_cycle = 0.3 * 90  # A DBF will store all EncIDs representing encounters faced during a 90-second period
# dbf_life_cycle = 2.5 * 60  # DBF that is older than 9 min from the current time is deleted from the node’s storage.
max_size = 100  # A node can only store maximum of 6 DBFs.

check_covid_cycle = 1 * 60  # check node if positive every 3min
bloom_fiter_size = 100
node_id = 'Attacker'  # Generate a unique UUID for this node

dbf_list = []
dbf = BloomFilter(bloom_fiter_size)


def broadcast_shares(shares, ephid_hash, node_id):
    """Broadcast each share over UDP with 3 seconds interval and incorporate drop mechanism."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # for share in shares:
    msg = {'share': shares, 'ephid_hash': ephid_hash, 'node_id': node_id}
    msg_json = json.dumps(msg)
    sock.sendto(msg_json.encode(), (broadcast_ip, port))
    print_colored(f"Task 11-B\n"
                  f"Attacker broadcasting share: {shares}"
                  , 'green')


def receive_from_brdcast(sock):
    """receive ephids from udp broadcast"""
    data, _ = sock.recvfrom(1024)
    msg_json = data.decode()
    msg = json.loads(msg_json)
    share = msg.get('share')
    ephid_hash = msg.get('ephid_hash')
    sender_node_id = msg.get('node_id')
    return share, ephid_hash, sender_node_id


def disrupt_shares(node_id=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind(('', port))
    shares = []

    while True:
        share, ephid_hash, sender_node_id = receive_from_brdcast(sock)
        # if len(shares) > 10:
        broadcast_shares(share, ephid_hash, node_id)


def main():
    disrupt_shares("attacker")


if __name__ == '__main__':
    main()
