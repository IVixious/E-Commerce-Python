import hashlib

from datetime import datetime

class Manager:
    def __init__(self):
        # System administration data
        self.users = {}  # Dictionary to store user accounts with hashed passwords

        # Order management data
        self.orders = {}  # Dictionary to store orders, by order ID

        # Financial management data
        self.finances = {'income': 0, 'expenses': 0}  # Track income and expenses

        # Inventory data
        self.inventory = {}  # Dictionary to store inventory items

        # Customer feedback data
        self.feedback = []  # List to store customer feedback

    # Utility method for password hashing
    def _hash_password(self, password):
        """Hashes a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    # 1. System Administration
    def add_user(self, username, password):
        """Adds a user with a hashed password."""
        if not username or not password:
            print("Username and password cannot be empty.")
            return

        if username in self.users:
            print(f"User '{username}' already exists.")
        else:
            self.users[username] = self._hash_password(password)
            print(f"User '{username}' added.")

    def remove_user(self, username):
        """Removes a user if they exist."""
        if username in self.users:
            del self.users[username]
            print(f"User '{username}' removed.")
        else:
            print("User not found.")

    def verify_credentials(self, username, password):
        """Verifies if the provided username and password are correct."""
        if not username or not password:
            print("Username and password cannot be empty.")
            return False

        if username in self.users:
            hashed_password = self._hash_password(password)
            if self.users[username] == hashed_password:
                return True

        print("Incorrect username or password.")
        return False

    # 2. Order Management
    def add_order(self, order_id, details):
        """Adds a new order if it doesn't already exist and validates the details."""
        if not order_id.strip():  # Check if order_id is empty or only contains spaces
            print("Order ID cannot be empty.")
            return

        if order_id in self.orders:
            print(f"Order '{order_id}' already exists. Use a different ID or update the existing order.")
            return

        if not isinstance(details, dict) or "status" not in details or "items" not in details:
            print("Invalid order details. Please provide a dictionary with 'status' and 'items'.")
            return

        self.orders[order_id] = details
        print(f"Order '{order_id}' added with details: {details}")

    def update_order_status(self, order_id, status):
        """Updates the status of an existing order."""
        if not order_id.strip():  # Check if order_id is empty or only contains spaces
            print("Order ID cannot be empty.")
            return

        if order_id in self.orders:
            if "status" in self.orders[order_id]:
                self.orders[order_id]["status"] = status
                print(f"Order '{order_id}' updated successfully. New status: '{status}'.")
            else:
                print(f"Order '{order_id}' does not have a 'status' field.")
        else:
            print(f"Order '{order_id}' not found. Unable to update status.")

    # 3. Financial Management
    def add_income(self, amount):
        """Adds income to the finances if the amount is valid."""
        if not isinstance(amount, (int, float)) or amount <= 0:
            print("Error: Income amount must be a positive number.")
            return

        self.finances['income'] += amount
        print(f"Income updated. Total income: {self.finances['income']}.")

    def add_expense(self, amount):
        """Adds an expense to the finances if the amount is valid."""
        if not isinstance(amount, (int, float)) or amount <= 0:
            print("Error: Expense amount must be a positive number.")
            return

        self.finances['expenses'] += amount
        print(f"Expenses updated. Total expenses: {self.finances['expenses']}.")

    def check_profitability(self):
        """Calculates and prints the profitability."""
        profit = self.finances['income'] - self.finances['expenses']
        print(f"Profitability: {profit}")
        return profit

    def add_inventory_item(self, item_name, quantity):
        """Adds a new inventory item if the name and quantity are valid."""
        if not item_name.strip():
            print("Error: Item name cannot be empty.")
            return

        if not isinstance(quantity, int) or quantity <= 0:
            print("Error: Quantity must be a positive integer.")
            return

        if item_name in self.inventory:
            print(f"Error: Item '{item_name}' already exists in the inventory.")
            update_choice = input("Do you want to update its quantity instead? (yes/no): ").strip().lower()
            if update_choice == "yes":
                new_quantity = int(input(f"Enter the additional quantity for '{item_name}': "))
                self.inventory[item_name] += new_quantity  # Directly update the inventory
                print(f"Inventory updated for '{item_name}': {self.inventory[item_name]}.")
            else:
                print(f"'{item_name}' was not added to the inventory.")
        else:
            self.inventory[item_name] = quantity
            print(f"Added '{item_name}' to inventory with quantity {quantity}.")

    def update_inventory(self, item_name, quantity):
        """Updates the quantity of an existing inventory item."""
        if not item_name.strip():
            print("Error: Item name cannot be empty.")
            return

        if not isinstance(quantity, int) or quantity <= 0:
            print("Error: Quantity must be a positive integer.")
            return

        if item_name in self.inventory:
            self.inventory[item_name] = quantity
            print(f"Inventory updated for '{item_name}': {self.inventory[item_name]}.")
        else:
            print(f"Error: Item '{item_name}' not found in inventory.")

    def remove_inventory_item(self, item_name):
        """Removes an item from the inventory."""
        if not item_name.strip():
            print("Error: Item name cannot be empty.")
            return

        if item_name in self.inventory:
            del self.inventory[item_name]
            print(f"'{item_name}' removed from inventory.")
        else:
            print(f"Error: Item '{item_name}' not found in inventory.")

    # 5. Customer Feedback

    def add_feedback(self, feedback_text):
        """Adds customer feedback after validating its content."""
        if not feedback_text.strip():
            print("Error: Feedback cannot be empty.")
            return

        if len(feedback_text) > 200:
            print("Error: Feedback is too long. Please limit to 200 characters.")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.feedback.append({"text": feedback_text, "timestamp": timestamp})
        print("Feedback added successfully.")

    def view_feedback(self):
        """Displays all feedback, showing timestamps for context."""
        if self.feedback:
            print("\n--- Customer Feedback ---")
            for i, fb in enumerate(self.feedback, 1):
                print(f"{i}. {fb['text']} (Added on {fb['timestamp']})")
        else:
            print("No feedback available.")


def main():
    manager = Manager()

    # Add a sample user for testing login functionality
    manager.add_user("MsImpeccable", "Isha181901")

    while True:
        # Login section
        print("\n--- Login ---")
        username = input("Enter username: ")
        password = input("Enter password: ")

        # Verify credentials
        if manager.verify_credentials(username, password):
            print("Login successful!\n")
            # Once logged in, enter the management menu
            while True:
                print("\n--- Manager Menu ---")
                print("1. System Administration")
                print("2. Order Management")
                print("3. Financial Management")
                print("4. Inventory Control")
                print("5. Customer Feedback")
                print("6. Logout")
                choice = input("Please select an option (1-6): ")

                if choice == "1":
                    print("\n-- System Administration --")
                    sub_choice = input("1. Add User\n2. Remove User\nSelect option (1-2): ")
                    if sub_choice == "1":
                        username = input("Enter username: ")
                        password = input("Enter password: ")
                        manager.add_user(username, password)
                    elif sub_choice == "2":
                        username = input("Enter username to remove: ")
                        manager.remove_user(username)

                elif choice == "2":
                    print("\n-- Order Management --")
                    sub_choice = input("1. Add Order\n2. Update Order Status\nSelect option (1-2): ")
                    if sub_choice == "1":
                        order_id = input("Enter order ID: ")
                        status = input("Enter order status: ")
                        items = input("Enter items (comma separated): ").split(",")
                        manager.add_order(order_id, {"status": status, "items": items})
                    elif sub_choice == "2":
                        order_id = input("Enter order ID to update: ")
                        status = input("Enter new status: ")
                        manager.update_order_status(order_id, status)

                elif choice == "3":
                    print("\n-- Financial Management --")
                    sub_choice = input("1. Add Income\n2. Add Expense\n3. Check Profitability\nSelect option (1-3): ")
                    if sub_choice == "1":
                        amount = float(input("Enter income amount: "))
                        manager.add_income(amount)
                    elif sub_choice == "2":
                        amount = float(input("Enter expense amount: "))
                        manager.add_expense(amount)
                    elif sub_choice == "3":
                        manager.check_profitability()

                elif choice == "4":
                    print("\n-- Inventory Control --")
                    sub_choice = input("1. Add Inventory Item\n2. Update Inventory\n3. Remove Inventory Item\nSelect option (1-3): ")
                    if sub_choice == "1":
                        item_name = input("Enter item name: ")
                        quantity = int(input("Enter quantity: "))
                        manager.add_inventory_item(item_name, quantity)
                    elif sub_choice == "2":
                        item_name = input("Enter item name to update: ")
                        quantity = int(input("Enter new quantity: "))
                        manager.update_inventory(item_name, quantity)
                    elif sub_choice == "3":
                        item_name = input("Enter item name to remove: ")
                        manager.remove_inventory_item(item_name)

                elif choice == "5":
                    print("\n-- Customer Feedback --")
                    sub_choice = input("1. Add Feedback\n2. View Feedback\nSelect option (1-2): ")
                    if sub_choice == "1":
                        feedback_text = input("Enter feedback: ")
                        manager.add_feedback(feedback_text)
                    elif sub_choice == "2":
                        manager.view_feedback()

                elif choice == "6":
                    print("Logging out...")
                    logout_choice = input("\nWould you like to log back in? (yes/no): ").strip().lower()
                    if logout_choice != "yes":
                        print("Exiting the system. Goodbye!")
                        return
                    else:
                        break

                else:
                    print("Invalid option, please try again.")

        else:
            print("Incorrect username or password. Please try again.")

if __name__ == "__main__":
    main()
