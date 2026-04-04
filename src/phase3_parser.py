#  DataFlow Pro — Phase 3: The DAX Formula Parser (Stacks)
#  Business Goal: Evaluate custom KPI formulas on the fly.
import re
# ══════════════════════════════════════════════════════════════════════════════
#  Stack Implementations
# ══════════════════════════════════════════════════════════════════════════════
class ArrayStack:
    """Stack built on top of a Python list (array-backed)."""
    def __init__(self):
        self._data = []
    def push(self, val):
        self._data.append(val)
    def pop(self):
        if self.is_empty():
            raise IndexError("Stack underflow — cannot pop from an empty stack")
        return self._data.pop()
    def peek(self):
        return self._data[-1] if self._data else None
    def is_empty(self) -> bool:
        return len(self._data) == 0
    def __len__(self):
        return len(self._data)
    def __repr__(self):
        return f"ArrayStack({self._data})"
class _StackNode:
    """Internal node for the linked-list stack."""
    def __init__(self, data):
        self.data = data
        self.next = None
class LinkedListStack:
    """Stack built on top of a singly linked list (no array resizing)."""
    def __init__(self):
        self._top   = None
        self._count = 0
    def push(self, val):
        node      = _StackNode(val)
        node.next = self._top
        self._top = node
        self._count += 1
    def pop(self):
        if self.is_empty():
            raise IndexError("Stack underflow — cannot pop from an empty stack")
        data      = self._top.data
        self._top = self._top.next
        self._count -= 1
        return data
    def peek(self):
        return self._top.data if self._top else None
    def is_empty(self) -> bool:
        return self._count == 0
    def __len__(self):
        return self._count
    def __repr__(self):
        items, node = [], self._top
        while node:
            items.append(str(node.data))
            node = node.next
        return f"LinkedListStack([{', '.join(reversed(items))}])"
# ══════════════════════════════════════════════════════════════════════════════
#  DAX Expression Evaluator
# ══════════════════════════════════════════════════════════════════════════════
# Operator precedence (higher = evaluated first)
PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
def tokenize(expression: str) -> list:
    """
    Split a mathematical expression into a flat list of tokens.
    Handles multi-digit numbers, decimals, and all four operators + parentheses.

    Example:
        "(Revenue - Cost) * 0.14"  →  ['(', 'Revenue', '-', 'Cost', ')', '*', '0.14']
    """
    return re.findall(r'\d+\.?\d*|[+\-*/()]|[A-Za-z_]\w*', expression)
def check_balanced_parentheses(expression: str) -> bool:
    """
    Use a Stack to verify that every '(' has a matching ')'.
    Returns True if balanced, False otherwise.
    """
    stack = ArrayStack()
    for ch in expression:
        if ch == '(':
            stack.push(ch)
        elif ch == ')':
            if stack.is_empty():
                return False   # closing bracket with no matching open
            stack.pop()
    return stack.is_empty()    # True only if all opens were matched


def infix_to_postfix(tokens: list) -> list:
    """
    Convert an infix token list to postfix (Reverse Polish Notation)
    using the Shunting-Yard algorithm with a Stack.

    Infix  :  ( 3 + 5 ) * 2
    Postfix:  3 5 + 2 *
    """
    output   = []
    op_stack = ArrayStack()

    for token in tokens:
        if re.fullmatch(r'\d+\.?\d*', token):
            # Numeric literal → goes straight to output
            output.append(token)
        elif token in PRECEDENCE:
            # Operator: pop higher/equal precedence operators first
            while (not op_stack.is_empty() and
                   op_stack.peek() in PRECEDENCE and
                   PRECEDENCE[op_stack.peek()] >= PRECEDENCE[token]):
                output.append(op_stack.pop())
            op_stack.push(token)
        elif token == '(':
            op_stack.push(token)
        elif token == ')':
            # Pop until we find the matching '('
            while not op_stack.is_empty() and op_stack.peek() != '(':
                output.append(op_stack.pop())
            if op_stack.is_empty():
                raise ValueError("Mismatched parentheses — extra ')'")
            op_stack.pop()   # discard the '('
    # Flush remaining operators
    while not op_stack.is_empty():
        op = op_stack.pop()
        if op in ('(', ')'):
            raise ValueError("Mismatched parentheses — extra '('")
        output.append(op)
    return output
def evaluate_postfix(postfix_tokens: list) -> float:
    """
    Evaluate a postfix token list using a Stack.

    Algorithm:
      - Number  → push onto stack
      - Operator → pop two operands, apply operator, push result
    """
    stack = LinkedListStack()   # using the linked-list version here
    for token in postfix_tokens:
        if re.fullmatch(r'\d+\.?\d*', token):
            stack.push(float(token))
        else:
            if len(stack) < 2:
                raise ValueError(f"Invalid expression — not enough operands for '{token}'")
            b = stack.pop()   # second operand (popped first)
            a = stack.pop()   # first  operand
            if   token == '+': stack.push(a + b)
            elif token == '-': stack.push(a - b)
            elif token == '*': stack.push(a * b)
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("Division by zero detected in DAX formula")
                stack.push(a / b)
    if len(stack) != 1:
        raise ValueError("Invalid expression — too many operands")
    return stack.pop()
# ══════════════════════════════════════════════════════════════════════════════
#  Public API
# ══════════════════════════════════════════════════════════════════════════════
class DAXEvaluator:
    """
    Parses and evaluates NileMart DAX-style KPI expressions.
    Usage:
        engine = DAXEvaluator()
        result = engine.evaluate("(Revenue - Cost) * Tax_Rate",
                                 {"Revenue": 500000, "Cost": 320000, "Tax_Rate": 0.14})
        # → 25200.0
    """
    def evaluate(self, expression: str, variables: dict = None) -> float:
        """
        Substitute named variables then compute the numeric result.
        Parameters
        ----------
        expression : str
            A math expression, optionally containing variable names.
        variables  : dict, optional
            Mapping of variable name → numeric value.

        Returns
        -------
        float
            The evaluated result.
        """
        expr = expression
        # 1. Substitute variables
        if variables:
            for var, val in variables.items():
                expr = expr.replace(var, str(val))
        # 2. Validate parentheses
        if not check_balanced_parentheses(expr):
            raise ValueError(f"Unbalanced parentheses in: '{expression}'")
        # 3. Tokenise → infix list
        tokens = tokenize(expr)
        # 4. Convert infix → postfix (Shunting-Yard)
        postfix = infix_to_postfix(tokens)
        # 5. Evaluate postfix with a Stack
        result = evaluate_postfix(postfix)
        return result
        
def run_phase3():
    print("\n==================================================")
    print("   Phase 3: DAX Formula Parser (Stacks)           ")
    print("==================================================")
    engine = DAXEvaluator()
    while True:
        print("\n  a. Evaluate a formula")
        print("  b. Back to Main Menu")
        choice = input("\n  Select an option: ").strip().lower()
        if choice == "a":
            expr = input("  Enter formula (e.g. (100 - 20) * 0.14): ").strip()
            try:
                result = engine.evaluate(expr)
                print(f"  Result: {result:,.4f}")
            except Exception as e:
                print(f"  Error: {e}")
        elif choice == "b":
            break
        else:
            print("  Invalid choice.")
