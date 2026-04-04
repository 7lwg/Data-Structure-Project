import sys
from phase1_indexer import run_phase1
from phase2_tracker import run_phase2
# ── Main menu ──────────────────────────────────────────────────
def main():
    while True:
        print("\n==================================================")
        print("   Welcome to DataFlow Pro - NileMart ETL Engine  ")
        print("==================================================")
        print("1. Run Phase 1: Query Optimizer (Sorting & Searching)")
        print("2. Run Phase 2: Applied Steps Tracker (Linked Lists)")  # ← uncommented
        # print("3. Evaluate DAX Formula (Stack)")
        # print("4. Ingest Live Data (Queue)")
        # print("5. Analyze Org Chart Sales (Trees)")
        print("6. Exit")
        choice = input("\nSelect an option: ")
        if choice == "1":
            run_phase1()
        elif choice == "2":           # ← added
            run_phase2()
        elif choice == "6":
            print("Shutting down DataFlow Pro. Masalama!")
            sys.exit()
        else:
            print("Feature not yet implemented or invalid choice.")


if __name__ == "__main__":
    main()