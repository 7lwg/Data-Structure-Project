import sys
from phase1_indexer import run_phase1
from phase2_tracker import AppliedStepsTracker


# ── Phase 2 runner ─────────────────────────────────────────────
def run_phase2():
    print("\n==================================================")
    print("   Phase 2: Applied Steps Tracker (Linked Lists)  ")
    print("==================================================")
    tracker = AppliedStepsTracker()
    while True:
        print("\n  Current Step:", tracker.get_current_step())
        print("  a. Add Step")
        print("  b. Undo")
        print("  c. Redo")
        print("  d. Show History")
        print("  e. Back to Main Menu")
        choice = input("\n  Select an option: ").strip().lower()
        if choice == "a":
            name = input("  Step name (e.g. Remove Nulls): ").strip()
            desc = input("  Description: ").strip()
            tracker.add_step(name, desc)
        elif choice == "b":
            tracker.undo()
        elif choice == "c":
            tracker.redo()
        elif choice == "d":
            tracker.display_history()
        elif choice == "e":
            break
        else:
            print("  Invalid choice.")


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