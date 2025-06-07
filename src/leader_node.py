# This is the main node that process block bla bla.
import os
from dotenv import load_dotenv
load_dotenv()
import threading
import signal
from mmb_layer0.node.node import Node
from mmb_layer0.p2p.udp_protocol import UDPProtocol
import time

def check_eligibility():
    if os.path.exists("validator_key"):
        return True

    return False


def setup_leader_node():

    master: Node = Node()
    master.import_key("validator_key")
    master.debug()

    _protocol = UDPProtocol(master.node_event_handler, 5000)
    master.set_origin("127.0.0.1:5000")
    
    # saver: PrismaSaver = PrismaSaver()
    
    # master.set_saver(saver)
    

    return master
