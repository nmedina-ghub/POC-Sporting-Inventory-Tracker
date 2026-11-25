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


def validate_line(lines):
    """Checks transaction formatting and verifies inventory availability for ADD, REMOVE, and SEARCH lines."""

    inventory = {}

    for row_number, line in enumerate(lines, start=1):
        parts = line.strip().split(",")
        command = parts[0].strip().upper()

        valid = True
        reason = ""
        quantity = None

        # Check ADD formatting
        if command == "ADD":
            if len(parts) != 4:
                valid = False
                reason = "Incorrect number of fields"

            elif not parts[1].strip() or not parts[3].strip():
                valid = False
                reason = "Missing item name or category"

            else:
                try:
                    quantity = int(parts[2].strip())

                    if quantity <= 0:
                        valid = False
                        reason = "Quantity must be positive"

                except ValueError:
                    valid = False
                    reason = "Quantity must be a number"

        # Check REMOVE formatting
        elif command == "REMOVE":
            if len(parts) != 3:
                valid = False
                reason = "Incorrect number of fields"

            elif not parts[1].strip():
                valid = False
                reason = "Missing item name"

            else:
                try:
                    quantity = int(parts[2].strip())

                    if quantity <= 0:
                        valid = False
                        reason = "Quantity must be positive"

                except ValueError:
                    valid = False
                    reason = "Quantity must be a number"

        # Check SEARCH formatting
        elif command == "SEARCH":
            if len(parts) != 2:
                valid = False
                reason = "Incorrect number of fields"

            elif not parts[1].strip():
                valid = False
                reason = "Missing item name"

        # Reject unknown commands
        else:
            valid = False
            reason = "Invalid command"

        # Check inventory only if the formatting is valid
        if valid:
            name = parts[1].strip().lower()

            # ADD items to inventory
            if command == "ADD":
                if name not in inventory:
                    inventory[name] = 0

                inventory[name] += quantity

            # Check REMOVE items from inventory
            elif command == "REMOVE":
                if name not in inventory:
                    valid = False
                    reason = "Item does not exist"

                elif inventory[name] < quantity:
                    valid = False
                    reason = "Not enough stock"

                else:
                    inventory[name] -= quantity

        # Print the final result for each row
        print(
            "Row", row_number,
            "|", valid,
            "|", reason,
            "|", line.strip()
        )

filepath = "data/athletic_transactions.txt"

lines = read_batch_file(filepath)

print("\n--- VALIDATION RESULTS ---")
validate_line(lines)

#test_lines = [
#    "ADD,Basketballs,0,Equipment",
#    "ADD,Basketballs,-5,Equipment",
#    "REMOVE,Basketballs,0",
#    "REMOVE,Basketballs,-3",
#    "ADD,Basketballs,5,Equipment",
#    "REMOVE,Basketballs,2"
#]
#
#for line in test_lines:
#    print(validate_line(line), "|", line)

# Testing functions with the data file:
#filepath = "data/athletic_transactions.txt"
#
#lines = read_batch_file(filepath)
#
#valid_count = 0
#invalid_count = 0
#
#for row_number, line in enumerate(lines, start=1):
#    result = validate_line(line)
#
#    if result:
#        valid_count += 1
#        print("Row", row_number, "| True |", line.strip())
#    else:
#        invalid_count += 1
#        print("Row", row_number, "| False |", line.strip())
#
#print("\nSUMMARY")
#print("Valid transactions:", valid_count)
#print("Invalid transactions:", invalid_count)
#print("Total transactions:", len(lines))


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
