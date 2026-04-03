import csv
import time
import os
import bisect

# --- 1. Sorting Algorithms (Phase 1 Requirements) ---

def bubble_sort(data, idx):
    """Slow O(n^2) algorithm."""
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j][idx] > data[j + 1][idx]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data

def insertion_sort(data, idx):
    """Slow O(n^2) algorithm."""
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and key[idx] < data[j][idx]:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
    return data

def selection_sort(data, idx):
    """Slow O(n^2) algorithm."""
    for i in range(len(data)):
        min_idx = i
        for j in range(i + 1, len(data)):
            if data[j][idx] < data[min_idx][idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
    return data

def merge_sort(data, idx):
    """Optimized O(n log n) algorithm."""
    if len(data) > 1:
        mid = len(data) // 2
        L = data[:mid]
        R = data[mid:]
        merge_sort(L, idx)
        merge_sort(R, idx)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i][idx] < R[j][idx]:
                data[k] = L[i]; i += 1
            else:
                data[k] = R[j]; j += 1
            k += 1
        while i < len(L):
            data[k] = L[i]; i += 1; k += 1
        while j < len(R):
            data[k] = R[j]; j += 1; k += 1
    return data

def quick_sort(data, idx):
    """Optimized O(n log n) algorithm."""
    if len(data) <= 1:
        return data
    pivot = data[len(data) // 2][idx]
    left = [x for x in data if x[idx] < pivot]
    middle = [x for x in data if x[idx] == pivot]
    right = [x for x in data if x[idx] > pivot]
    return quick_sort(left, idx) + middle + quick_sort(right, idx)

# --- 2. Search Algorithms (Lookup Engine) ---

def linear_search(data, target_id):
    """O(n) search for unsorted data."""
    for row in data:
        if row[0] == target_id:
            return row
    return None

def binary_search(data, target_id):
    """O(log n) search for sorted data."""
    low = 0
    high = len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid][0] == target_id:
            return data[mid]
        elif data[mid][0] < target_id:
            low = mid + 1
        else:
            high = mid - 1
    return None

# --- 3. Execution & Benchmarking ---

def load_data():
    file_path = os.path.join("data", "transactions.csv")
    transactions = []
    with open(file_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Convert TransactionID (0) and Amount (3) to numbers 
            row[0] = int(row[0]) 
            row[3] = float(row[3])
            transactions.append(row)
    return header, transactions

def run_phase1():
    header, data = load_data()
    print(f"Loaded {len(data)} records from NileMart dataset.\n")

    # Benchmarking Sorts
    algorithms = [
        ("Merge Sort", merge_sort),
        ("Quick Sort", quick_sort),
        ("Built-in Timsort", lambda d, i: sorted(d, key=lambda x: x[i]))
    ]
    
    
    for name, func in algorithms:
        temp_data = data.copy()
        start = time.time()
        func(temp_data, 0)
        print(f"✅ {name}: {time.time() - start:.4f} seconds")

    # Search Comparison
    target = data[5000][0] # Pick a middle ID to search for
    sorted_data = sorted(data, key=lambda x: x[0])

    print(f"\nSearching for Transaction ID: {target}")
    
    start = time.time()
    linear_search(data, target)
    print(f"Linear Search: {time.time() - start:.6f} seconds")

    start = time.time()
    binary_search(sorted_data, target)
    print(f"Binary Search: {time.time() - start:.6f} seconds")

    # Bisect Slicing (e.g., finding transactions with specific ID range)
    ids_only = [row[0] for row in sorted_data]
    idx = bisect.bisect_left(ids_only, target)
    print(f"Bisect Lookup index: {idx}")

if __name__ == "__main__":
    run_phase1()