import time
from collections import deque

# 1. The Manual Linked List Node (For the middle optimization step)
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedListQueue:
    """Manual Linked List implementation of a Queue (O(1) Enqueue/Dequeue)."""
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, data):
        new_node = Node(data)
        if self.tail is None:
            self.head = self.tail = new_node
            return
        self.tail.next = new_node
        self.tail = new_node

    def dequeue(self):
        if self.head is None:
            return None
        temp = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return temp.data

# 2. The Main Buffer Engine
class LiveIngestionQueue:
    def __init__(self):
        self.list_buffer = []           # Phase 4.1: The O(n) Trap
        self.ll_buffer = LinkedListQueue() # Phase 4.2: Manual Linked List
        self.deque_buffer = deque()     # Phase 4.3: Production Deque

    # --- Standard List (The Trap) ---
    def use_list(self, data_size):
        # Enqueue is O(1)
        for i in range(data_size):
            self.list_buffer.append(i)
        # Dequeue is O(n) because pop(0) shifts all elements
        start = time.time()
        while self.list_buffer:
            self.list_buffer.pop(0)
        return time.time() - start

    # --- Manual Linked List (The Logic) ---
    def use_linked_list(self, data_size):
        for i in range(data_size):
            self.ll_buffer.enqueue(i)
        start = time.time()
        while self.ll_buffer.head:
            self.ll_buffer.dequeue()
        return time.time() - start

    # --- Collections Deque (The Standard) ---
    def use_deque(self, data_size):
        for i in range(data_size):
            self.deque_buffer.append(i)
        start = time.time()
        while self.deque_buffer:
            self.deque_buffer.popleft()
        return time.time() - start

def run_phase4():
    print("\n--- Phase 4: Live Data Buffer (Queue Optimization) ---")
    buffer = LiveIngestionQueue()
    test_size = 30000  # 30k rows to clearly show the O(n) slowdown
    
    print(f"Simulating {test_size} White Friday transactions...")

    # Test 1: List
    list_time = buffer.use_list(test_size)
    print(f"1. Standard List pop(0) [O(n)]: {list_time:.4f}s")

    # Test 2: Linked List
    ll_time = buffer.use_linked_list(test_size)
    print(f"2. Manual Linked List [O(1)]:   {ll_time:.4f}s")

    # Test 3: Deque
    deque_time = buffer.use_deque(test_size)
    print(f"3. Production Deque [O(1)]:    {deque_time:.4f}s")

if __name__ == "__main__":
    run_phase4()