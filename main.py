
import time
from src.leader_node import setup_leader_node, check_eligibility
from mmb_layer0.node.node import Node

if __name__ == '__main__':
    master = None
    try:
        if not check_eligibility():
            print("You are not eligible to be a leader node.")
            exit(0)
        else:
            print("You are eligible to be a leader node.")
        master: Node = setup_leader_node()

        while True:
            time.sleep(1)
    except Exception as e:
        import traceback
        print("An error occurred:", e)
        traceback.print_exc()
        print("Shutting down gracefully...")

        master.save_chain_to_disk()