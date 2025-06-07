from mmb_layer0.blockchain.chain.local_saver import ISaver
from mmb_layer0.blockchain.core.chain import Chain
from mmb_layer0.blockchain.core.block import Block
import asyncio
import threading
import time
from concurrent.futures import Future, TimeoutError
from typing import Callable, Any, Optional
from prisma import Prisma
from src.asyncioconversion import AsyncToThread

class PrismaSaver(ISaver):

    def __init__(self) -> None:
        self.async_to_thread = AsyncToThread()
        self.db = Prisma()
        self.connected = False
        self.connect()
        
    def connect(self) -> None:
        # Connect to the Prisma database
        print("Connecting to the database...")
        self.async_to_thread.run_async(self.db.connect(), callback=self._on_connect)
        
    def _on_connect(self, result: Any) -> None:
        if isinstance(result, Exception):
            print(f"Failed to connect to the database: {result}")
        else:
            print("Connected to the database successfully.")
        self.connected = True
    
    def save_chain(self, chain: "Chain") -> None:
        pass
    
    def load_chain(self) -> "Chain":
        # This method should load the chain from the database
        return Chain()
    
    def add_block(self, block: "Block") -> None:
        pass
