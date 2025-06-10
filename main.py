
import time
from mmb_layer0.node.node import Node
# This is the main node that process block bla bla.
import os
from dotenv import load_dotenv
load_dotenv()
import threading
import signal
from mmb_layer0.node.node import Node
from mmb_layer0.p2p.udp_protocol import UDPProtocol
from mmb_layer0.p2p.peer_type.remote_peer import RemotePeer
import time
import sys
import requests

def get_public_ip():
    # return "127.0.0.1" # For testing purposes, we use localhost. In production, you would use a real public IP.
    try:
        # Using ipify.org (a popular and free service)
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error: Could not retrieve IP from ipify.org. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def check_eligibility():
    if os.path.exists("validator_key.priv"):
        return True
    return False

    
def setup_leader_node(port: int = 5000) -> Node:

    master: Node = Node()
    master.import_key("validator_key")
    master.debug()
    _protocol = UDPProtocol(master.node_event_handler, port)
    master.set_origin(f"{get_public_ip()}:{port}") # Leader node runs on port 5000

    return master

def setup_follower_node(port: int = 5000) -> Node:
    follower: Node = Node()
    follower.debug()
    _protocol = UDPProtocol(follower.node_event_handler, port)
    follower.set_origin(f"{get_public_ip()}:{port}")
    
    # Genesis boostrap
    for line in open("boostrap.txt", "r"):
        line = line.strip()
        if not line:
            continue
        p_ip: str = line.split(":")[0]
        p_port: int = int(line.split(":")[1])
        peer: RemotePeer = RemotePeer(p_ip, p_port)
        
        follower.node_event_handler.subscribe(peer)
    
    return follower


def master_path(port: int = 5000) -> None   :
    master: Node = setup_leader_node(port)
    try:
        while True:
            time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        master.save_chain_to_disk()

def follower_path(port: int = 5000) -> None:
    follower: Node = setup_follower_node(port)
    try:
        while True:
            time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        follower.save_chain_to_disk()

if __name__ == '__main__':
    
    port: int = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    
    if not check_eligibility():
        print("You are eligible to be a follower node.")
        follower_path(port)
    else:
        print("You are eligible to be a leader node.")
        master_path(port)
    