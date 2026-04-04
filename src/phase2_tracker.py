#  DataFlow Pro — Phase 2: The "Applied Steps" Tracker (Linked Lists)
#  Business Goal: Recreate Power Query's transformation tracking system.
# ── Node for the Doubly Linked List ───────────────────────────────────────────
class StepNode:
    def __init__(self, name: str, description: str):
        self.name        = name
        self.description = description
        self.prev        = None   # pointer to previous step
        self.next        = None   # pointer to next step
# ── Singly Linked List (Step 1 — basic history) ───────────────────────────────
class SinglyStepsTracker:
    """
    Simple singly linked list where each node is a transformation step.
    Supports append and forward traversal only.
    """
    def __init__(self):
        self.head  = None
        self._size = 0
    def add_step(self, name: str, description: str) -> None:
        """Append a new step to the end of the list — O(n)."""
        node = StepNode(name, description)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node
        self._size += 1
    def display_history(self) -> None:
        """Print all recorded steps from head to tail."""
        print("\n  [Singly] Applied Steps History:")
        node = self.head
        while node:
            arrow = "→" if node.next else "■"
            print(f"     {arrow}  {node.name}: {node.description}")
            node = node.next
    def __len__(self):
        return self._size
# ── Doubly Linked List (Step 2 — undo / redo engine) ─────────────────────────
class AppliedStepsTracker:
    """
    Doubly Linked List tracking every Power Query transformation step.
    Supports O(1) undo and redo — analysts can navigate back and forward
    through their transformation history without reloading the dataset.
    """
    def __init__(self):
        self.head    = None
        self.current = None   # always points to the active step
        self._size   = 0
    # ── Core Operations ───────────────────────────────────────────────────────
    def add_step(self, name: str, description: str) -> None:
        """
        Append a new transformation step after the current position.
        If the analyst undid some steps and then adds a new one,
        the 'future' branch is discarded (same behaviour as Power Query).
        """
        node = StepNode(name, description)

        if self.head is None:
            # Very first step
            self.head    = node
            self.current = node
        else:
            # Truncate any future steps beyond the current position
            if self.current.next:
                self.current.next = None   # cut the forward chain

            # Link new node
            node.prev        = self.current
            self.current.next = node
            self.current     = node

        self._size += 1
        print(f"  ➕  Step added   : [{name}] — {description}")

    def undo(self) -> None:
        """
        Move one step BACKWARD — O(1).
        Mimics pressing Ctrl+Z in Power Query.
        """
        if self.current is None or self.current.prev is None:
            print("  ⚠️   Nothing to undo. Already at the first step.")
            return
        self.current = self.current.prev
        print(f"  ↩️   Undo  → now at: [{self.current.name}]")
    def redo(self) -> None:
        """
        Move one step FORWARD — O(1).
        Mimics pressing Ctrl+Y in Power Query.
        """
        if self.current is None or self.current.next is None:
            print("  ⚠️   Nothing to redo. Already at the latest step.")
            return
        self.current = self.current.next
        print(f"  ↪️   Redo  → now at: [{self.current.name}]")

    def get_current_step(self) -> str:
        """Return the name of the currently active step."""
        return self.current.name if self.current else "No steps recorded"
    # ── Display ───────────────────────────────────────────────────────────────
    def display_history(self) -> None:
        """Print the full step history, highlighting the current step."""
        print("\n  [Doubly] Applied Steps History:")
        node = self.head
        idx  = 1
        while node:
            marker = " ◀◀ (CURRENT)" if node is self.current else ""
            arrow  = "→" if node.next else "■"
            print(f"     {idx:>2}. {arrow}  {node.name}{marker}")
            print(f"         └─ {node.description}")
            node = node.next
            idx += 1
    def __len__(self):
        return self._size

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
