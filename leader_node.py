# This is the main node that process block bla bla.

import os
import threading
import signal
from mmb_layer0.node.node import Node
from mmb_layer0.p2p.udp_protocol import UDPProtocol

def check_eligibility():
    if os.path.exists("validator_key"):
        return True

    return False

def signal_handler(_sig, _frame):
    print("Shutting down gracefully...")
    stop_event.set()

def setup_leader_node():

    master = Node()
    master.import_key("validator_key")
    master.debug()

    _protocol = UDPProtocol(master.node_event_handler, 5000)
    master.set_origin("127.0.0.1:5000")

    return master

if __name__ == '__main__':
    if not check_eligibility():
        print("You are not eligible to be a leader node.")
        exit(0)
    else:
        print("You are eligible to be a leader node.")

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    stop_event = threading.Event()

    master = setup_leader_node()

    stop_event.wait()

    print("Shutting down gracefully...")

    master.save_chain_to_disk()