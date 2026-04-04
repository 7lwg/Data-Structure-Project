from anytree import Node, RenderTree

# --- Part 1: The Dimension Index (Binary Search Tree) ---
class BSTNode:
    def __init__(self, national_id, customer_name):
        self.national_id = int(national_id)
        self.name = customer_name
        self.left = None
        self.right = None

class DimensionIndex:
    """BST to mimic Power BI's internal compression of Dimension Tables."""
    def __init__(self):
        self.root = None

    def insert(self, national_id, name):
        if not self.root:
            self.root = BSTNode(national_id, name)
        else:
            self._insert_recursive(self.root, national_id, name)

    def _insert_recursive(self, current, national_id, name):
        if national_id < current.national_id:
            if current.left is None:
                current.left = BSTNode(national_id, name)
            else:
                self._insert_recursive(current.left, national_id, name)
        elif national_id > current.national_id:
            if current.right is None:
                current.right = BSTNode(national_id, name)
            else:
                self._insert_recursive(current.right, national_id, name)

    def search(self, national_id):
        """O(log n) retrieval for relationships."""
        return self._search_recursive(self.root, national_id)

    def _search_recursive(self, current, national_id):
        if current is None: return None
        if current.national_id == national_id: return current.name
        if national_id < current.national_id:
            return self._search_recursive(current.left, national_id)
        return self._search_recursive(current.right, national_id)

# --- Part 2 & 3: The Organizational Chart & Roll-Up Task ---
class OrgChartAnalyzer:
    """Models NileMart Corporate Hierarchy using N-ary Trees."""
    
    def __init__(self):
        # Initializing nodes with 'sales' attribute for the Roll-Up task
        self.ceo = Node("Omar (Global CEO)", sales=0)
        
        # Regional VPs
        self.vp_cairo = Node("Tarek (VP Cairo)", parent=self.ceo, sales=0)
        self.vp_alex = Node("Salma (VP Alex)", parent=self.ceo, sales=0)

        # Store Managers
        self.mngr_maadi = Node("Hoda (Maadi Manager)", parent=self.vp_cairo, sales=0)
        self.mngr_smouha = Node("Kareem (Smouha Manager)", parent=self.vp_alex, sales=0)

        # Sales Reps (The leaves with actual revenue)
        Node("Rep_1", parent=self.mngr_maadi, sales=50000)
        Node("Rep_2", parent=self.mngr_maadi, sales=75000)
        Node("Rep_3", parent=self.mngr_smouha, sales=120000)

    def display_structure(self):
        print("\n[NileMart Org Structure]:")
        for pre, _, node in RenderTree(self.ceo):
            print(f"{pre}{node.name}")

    def roll_up_sales(self, node):
        """
        Recursive traversal: Sums current node sales + all children sales.
        Essential for 'Matrix' visuals in Power BI.
        """
        total = node.sales
        for child in node.children:
            total += self.roll_up_sales(child)
        return total

def run_phase5():
    print("\n--- Phase 5: Hierarchical Matrix Builder (Trees) ---")
    
    # Testing BST Indexing
    index = DimensionIndex()
    # Using sample Egyptian National IDs (simplified)
    index.insert(2990505, "Ahmed Hassan")
    index.insert(2800101, "Sara Ali")
    
    print(f"Searching ID 2990505... Result: {index.search(2990505)}")

    # Testing Org Chart & Roll-Up
    org = OrgChartAnalyzer()
    org.display_structure()
    
    cairo_revenue = org.roll_up_sales(org.vp_cairo)
    print(f"\nTotal Revenue Roll-up for VP Cairo: {cairo_revenue:,} EGP")
    
    total_company = org.roll_up_sales(org.ceo)
    print(f"Total Company Revenue: {total_company:,} EGP")

if __name__ == "__main__":
    run_phase5()
