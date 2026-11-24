"""
Command-line inventory tracker -- you choose the scenario.

See ../PROJECT_OVERVIEW.md to pick your stakeholder and data file. Design your own
class for one inventory item, based on what *your* stakeholder needs.
There's no single right set of attributes, and that's on purpose.

Run it from your repo's top folder (not from inside this folder):
    python3 starter/inventory.py
Before your final push you'll rename this folder to analysis/.
"""
import json

class SportsInventoryItem:
    """Represents one item in a sporting goods inventory. Tracks the product name, quantity, category, and low-stock limit."""

    def __init__(self, name, quantity, category, low_stock_limit=10):
        self.name = name
        self.quantity = quantity
        self.category = category
        self.low_stock_limit = low_stock_limit

    def is_low_stock(self):
        """Checks whether the item quantity is below low_stock_limit."""
        
        return self.quantity < self.low_stock_limit

# Tested class with two different objects:
#item1 = SportsInventoryItem("Running Shoes (M)", 48, "Footwear")
#item2 = SportsInventoryItem("Yoga Mats", 9, "Equipment")
#print(item1.name, item1.quantity, item1.category)
#print("Low stock:", item1.is_low_stock())
#print(item2.name, item2.quantity, item2.category)
#print("Low stock:", item2.is_low_stock())


def read_batch_file(filepath):
    """Reads the batch file and returns its lines unchanged as a list."""
    
    with open(filepath, "r") as file:
        lines = file.readlines()

    return lines


def validate_line(line):
    """Checks whether an ADD, REMOVE, or SEARCH line has the correct format and required fields, returning True if valid and False if invalid."""

    parts = line.strip().split(",")
    command = parts[0].strip().upper()

    if command == "ADD":
        if len(parts) != 4:
            return False

        if not parts[1].strip() or not parts[3].strip():
            return False

        try:
            int(parts[2].strip())
        except ValueError:
            return False

        return True

    elif command == "REMOVE":
        if len(parts) != 3:
            return False

        if not parts[1].strip():
            return False

        try:
            int(parts[2].strip())
        except ValueError:
            return False

        return True

    elif command == "SEARCH":
        if len(parts) != 2:
            return False

        if not parts[1].strip():
            return False

        return True

    return False


def process_transactions(lines):
    """TODO: write your own docstring."""
    # TODO: implement. Loop over the lines, apply each valid one to your
    # collection of items, and print a specific message for each line
    # you skip. Return the collection at the end. The full inventory
    # printout is print_summary's job, not this function's.
    pass


def find_item(items, name):
    """TODO: write your own docstring."""
    # TODO: implement
    pass


def export_to_json(items, filepath="inventory.json"):
    """TODO: write your own docstring. json.dump can't write your objects
    directly, so turn each one into a dict first."""
    # TODO: implement
    pass


def print_summary(items):
    """TODO: write your own docstring."""
    # TODO: implement. This one only prints, so it doesn't need to return
    # anything.
    pass


# TODO: point this at the data file for the scenario you chose.
lines = read_batch_file("data/____________.txt")
items = process_transactions(lines)
print_summary(items)
export_to_json(items)
