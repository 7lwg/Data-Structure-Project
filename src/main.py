import sys
# Import the run function from your phase 1 script
from phase1_indexer import run_phase1 

def main():
    while True:
        print("\n==================================================")
        print("   Welcome to DataFlow Pro - NileMart ETL Engine  ")
        print("==================================================")
        print("1. Run Phase 1: Query Optimizer (Sorting & Searching)")
        # print("2. Add ETL Step (Linked List)")
        # print("3. Evaluate DAX Formula (Stack)")
        # print("4. Ingest Live Data (Queue)")
        # print("5. Analyze Org Chart Sales (Trees)")
        print("6. Exit")

        choice = input("\nSelect an option: ")

        if choice == "1":
            # Call the function from phase1_indexer.py
            run_phase1()
        
        elif choice == "6":
            print("Shutting down DataFlow Pro. Masalama!")
            sys.exit()
        else:
            print("Feature not yet implemented or invalid choice.")

if __name__ == "__main__":
    main()