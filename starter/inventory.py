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
        """Initializes a sports inventory item with its name, quantity, category, and low-stock limit."""
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

# Reads the transaction file and returns all lines as a list
# so they can be checked individually by the validation function.
def read_batch_file(filepath):
    """Reads the batch file and returns its lines unchanged as a list."""
    
    with open(filepath, "r") as file:
        lines = file.readlines()

    return lines

# Checks each transaction for formatting errors and verifies that
# ADD, REMOVE, and SEARCH operations make sense with the current inventory.
# Prints whether each line is valid or invalid, along with the reason.
def validate_line(lines):
    """Checks transaction formatting and verifies inventory availability for ADD, REMOVE, and SEARCH lines."""

    inventory = {}

    for row_number, line in enumerate(lines, start=1):

        # Handle blank lines
        if not line.strip():
            print(f"Row {row_number} | False | Blank line |")
            continue

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

        # Reject unknown entries
        else:
            valid = False
            reason = "Invalid entry"

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

            # Check SEARCH items in inventory
            elif command == "SEARCH":
                if name not in inventory:
                    valid = False
                    reason = "Item does not exist"

        # Print the final result for each row
        print(
            "Row", row_number,
            "|", valid,
            "|", reason,
            "|", line.strip()
        )

#Testing functions with the data file:
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
#
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
    """Processes valid transactions and updates the inventory."""

    inventory = []

    for line in lines:
        parts = line.strip().split(",")

        # Skip blank lines
        if not line.strip():
            print("Skipping blank line")
            continue

        command = parts[0].strip().upper()

        try:
            # ADD items
            if command == "ADD":
                if len(parts) != 4:
                    print(f"Skipping ADD: incorrect number of fields | {line.strip()}")
                    continue

                name = parts[1].strip()
                quantity = int(parts[2].strip())
                category = parts[3].strip()

                if not name or not category:
                    print(f"Skipping ADD: missing name or category | {line.strip()}")
                    continue

                if quantity <= 0:
                    print(f"Skipping ADD: quantity must be positive | {line.strip()}")
                    continue

                item = find_item(inventory, name)

                if item:
                    item.quantity += quantity
                else:
                    inventory.append(SportsInventoryItem(name, quantity, category))

            # REMOVE items
            elif command == "REMOVE":
                if len(parts) != 3:
                    print(f"Skipping REMOVE: incorrect number of fields | {line.strip()}")
                    continue

                name = parts[1].strip()
                quantity = int(parts[2].strip())

                if not name:
                    print(f"Skipping REMOVE: missing item name | {line.strip()}")
                    continue

                if quantity <= 0:
                    print(f"Skipping REMOVE: quantity must be positive | {line.strip()}")
                    continue

                item = find_item(inventory, name)

                if item:
                    if item.quantity >= quantity:
                        item.quantity -= quantity
                    else:
                        print(f"Skipping REMOVE: not enough stock for {name}")
                else:
                    print(f"Skipping REMOVE: {name} does not exist")

            # SEARCH items
            elif command == "SEARCH":
                if len(parts) != 2:
                    print(f"Skipping SEARCH: incorrect number of fields | {line.strip()}")
                    continue

                name = parts[1].strip()

                if not name:
                    print(f"Skipping SEARCH: missing item name | {line.strip()}")
                    continue

                item = find_item(inventory, name)

                if item:
                    print(f"Found: {item.name} | Quantity: {item.quantity} | Category: {item.category}")
                else:
                    print(f"Skipping SEARCH: {name} does not exist")

            # Invalid commands
            else:
                print(f"Skipping invalid command: {command}")

        except ValueError:
            print(f"Skipping transaction: quantity is not a valid number | {line.strip()}")

        except IndexError:
            print(f"Skipping transaction: missing fields | {line.strip()}")

    return inventory


def find_item(items, name):
    """Finds an inventory item by name and returns it, or None if not found."""

    for item in items:
        if item.name.lower() == name.lower():
            return item

    return None

# Temporary test for process_transactions:
#test_lines = [
#    "ADD,Yoga Mats,10,Equipment",
#    "ADD,Yoga Mats,5,Equipment",
#    "ADD,Basketballs,8,Equipment",
#    "REMOVE,Yoga Mats,3",
#    "SEARCH,Basketballs",
#    "REMOVE,Basketballs,99",
#    "REMOVE,Tennis Rackets,2",
#    "ADD,Running Shoes,five,Footwear",
#    "ADD,Jump Ropes,5",
#    "",
#    "HELLO,World"
#]
#
#test_inventory = process_transactions(test_lines)
#
#print("\n--- TEST INVENTORY RESULTS ---")
#for item in test_inventory:
#    print(f"{item.name}: {item.quantity} | {item.category}")


def export_to_json(items, filepath="inventory.json"):
    """Exports inventory items to a JSON file."""

    data = []

    for item in items:
        item_dict = {
            "name": item.name,
            "quantity": item.quantity,
            "category": item.category
        }

        data.append(item_dict)

    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Inventory exported to {filepath}")

def print_summary(items):
    """Prints a summary of all inventory items and their stock levels."""

    print(f"{'ITEM':<30} {'QUANTITY':<10} {'CATEGORY':<15} {'STOCK STATUS'}")
    print("-" * 75)

    for item in items:
        if item.is_low_stock():
            status = "LOW STOCK"
        else:
            status = "OK"

        print(f"{item.name:<30} {item.quantity:<10} {item.category:<15} {status}")

    print("-" * 75)
    print(f"Total unique items: {len(items)}")

# ================= MAIN PROGRAM =================

filepath = "data/athletic_transactions.txt"
lines = read_batch_file(filepath)

# Validation
print("\n========== VALIDATION RESULTS ==========")
validate_line(lines)

# Transaction processing
print("\n========== TRANSACTION PROCESSING ==========")
inventory = process_transactions(lines)

# Final inventory
print("\n========== FINAL INVENTORY ==========")
print_summary(inventory)

# Export inventory
print("\n========== EXPORTING INVENTORY ==========")
export_to_json(inventory)

