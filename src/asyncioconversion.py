import asyncio
import threading
from functools import wraps
import queue

class AsyncToThread:
    def __init__(self):
        # Queue to handle callbacks on the main thread
        self.callback_queue = queue.Queue()
        # Event loop for async tasks
        self.loop = asyncio.new_event_loop()
        # Thread for running the event loop
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        
    def _run_loop(self):
        print("Starting event loop in thread:", threading.current_thread().name)
        """Run the asyncio event loop in a separate thread."""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
        print("Event loop stopped")

    def run_async(self, coro, callback=None):
        """
        Run an async coroutine in the event loop thread and invoke callback on main thread.
        
        Args:
            coro: The asyncio coroutine to run.
            callback: Optional function to call with the result on the main thread.
        """
        def handle_result(future):
            try:
                result = future.result()
                if callback:
                    # Put the callback and result in the queue to be processed on main thread
                    self.callback_queue.put((callback, result))
            except Exception as e:
                if callback:
                    self.callback_queue.put((callback, e))
        
        # Schedule the coroutine in the event loop
        future = asyncio.run_coroutine_threadsafe(coro, self.loop)
        future.add_done_callback(handle_result)
    
    def process_callbacks(self):
        """
        Process pending callbacks on the main thread.
        Call this periodically in the main thread (e.g., in a game loop or main event loop).
        """
        while True:
            try:
                # Non-blocking check for callbacks
                callback, result = self.callback_queue.get_nowait()
                callback(result)
            except queue.Empty:
                break
    
    def wrap_async(self, coro_func):
        """
        Decorator to convert an async function into a threaded version with callback.
        
        Args:
            coro_func: The async function to wrap.
        
        Returns:
            A function that takes a callback and runs the coroutine off the main thread.
        """
        @wraps(coro_func)
        def wrapper(*args, callback=None, **kwargs):
            coro = coro_func(*args, **kwargs)
            self.run_async(coro, callback)
        return wrapper

    def stop(self):
        """Stop the event loop and thread."""
        # Wrap self.loop.stop in a lambda to match the expected callable signature
        self.loop.call_soon_threadsafe(lambda **kwargs: self.loop.stop())
        self.loop.run_until_complete(self.loop.shutdown_asyncgens())
        self.loop.close()