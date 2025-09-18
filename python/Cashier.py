import json

class CashierSystem:
    def __init__(self, file_name):
        self.file_name = file_name  # Store the JSON file name
        self.products = []  # List to store product catalog
        self.discounts = {}  # Dictionary to store discounts by product ID
        self.sales = []  # List to store completed transactions

        # Preloading products from the JSON file
        self.load_products_from_file()

    def load_products_from_file(self):
        """Loads the product list from the JSON file."""
        try:
            with open(self.file_name, 'r') as file:
                self.products = json.load(file)
                print(f"Products successfully loaded from '{self.file_name}'.")
        except FileNotFoundError:
            print(f"Error: '{self.file_name}' file not found.")
        except json.JSONDecodeError:
            print(f"Error: '{self.file_name}' contains invalid JSON.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def save_products_to_file(self):
        """Saves the current product list to the JSON file."""
        try:
            with open(self.file_name, 'w') as file:
                json.dump(self.products, file, indent=4)
                print(f"Products successfully saved to '{self.file_name}'.")
        except Exception as e:
            print(f"Error saving products to file: {e}")

    def add_product(self):
        """Adds a new product to the catalog."""
        print("\nAdd Product:")
        product_id = input("Enter product ID: ")

        # Check if the product ID already exists
        if any(product['id'] == product_id for product in self.products):
            print(f"Error: Product ID '{product_id}' already exists in the catalog.")
            return

        name = input("Enter product name: ")
        type_ = input("Enter product type (e.g., Beverage, Food, Pastry): ")
        details = input("Enter product details (optional): ")
        price = float(input("Enter product price (in RM): "))

        # Append the new product to the product catalog
        new_product = {"id": product_id, "name": name, "type": type_, "details": details, "price": price}
        self.products.append(new_product)

        # Save the updated products list to the JSON file
        self.save_products_to_file()
        print(f"Product '{name}' added to catalog.")

    def display_products(self):
        """Displays the product catalog."""
        print("\nProduct Catalog:")
        print(f"{'ID':<5} | {'Name':<25} | {'Type':<10} | {'Details':<20} | {'Price':<6}")
        print("-" * 70)
        for product in self.products:
            print(f"{product['id']:<5} | {product['name']:<25} | {product['type']:<10} | "
                  f"{product['details']:<20} | RM{product['price']:.2f}")

    def get_products_by_type(self, product_type):
        """Returns all products of a given type."""
        return [prod for prod in self.products if prod["type"] == product_type]

    def filter_products_by_category(self):
        """Displays products filtered by their category (type)."""
        print("\nFilter Products by Category:")
        category = input("Enter product type (e.g., Beverage, Food, Pastry): ").strip()
        filtered_products = self.get_products_by_type(category)

        if filtered_products:
            print(f"\nProducts in '{category}' Category:")
            print(f"{'ID':<5} | {'Name':<25} | {'Type':<10} | {'Details':<20} | {'Price':<6}")
            print("-" * 70)
            for product in filtered_products:
                print(f"{product['id']:<5} | {product['name']:<25} | {product['type']:<10} | "
                      f"{product['details']:<20} | RM{product['price']:.2f}")
        else:
            print(f"No products found in the '{category}' category.")

    def add_discount(self):
        """Adds or modifies a discount for a product or all products."""
        print("\nAdd Discount:")
        choice = input("1. Apply discount to a single product\n2. Apply discount to all products\nEnter your choice: ")

        if choice == "1":
            product_id = input("Enter product ID to apply discount: ")

            # Check if the product ID exists in the catalog
            if not any(product['id'] == product_id for product in self.products):
                print(f"Error: Product ID '{product_id}' does not exist in the catalog.")
                return

            try:
                discount = float(input("Enter discount percentage (0-100): "))
                if discount < 0 or discount > 100:
                    print("Error: Discount percentage must be between 0 and 100.")
                    return
                self.discounts[product_id] = discount
                print(f"Discount of {discount}% applied to product ID {product_id}.")
            except ValueError:
                print("Invalid input. Please enter a valid percentage.")

        elif choice == "2":
            try:
                discount = float(input("Enter discount percentage for all products (0-100): "))
                if discount < 0 or discount > 100:
                    print("Error: Discount percentage must be between 0 and 100.")
                    return
                # Apply discount to all products
                for product in self.products:
                    self.discounts[product['id']] = discount
                print(f"Discount of {discount}% applied to all products.")
            except ValueError:
                print("Invalid input. Please enter a valid percentage.")
        else:
            print("Invalid choice. Please try again.")

    def view_active_discounts(self):
        """Displays all active discounts for products."""
        print("\nActive Discounts:")
        if not self.discounts:
            print("No active discounts.")
        else:
            print(f"{'ID':<5} | {'Product Name':<25} | {'Discount (%)':<10}")
            print("-" * 50)
            for product_id, discount in self.discounts.items():
                # Find the product by its ID
                product = next((p for p in self.products if p['id'] == product_id), None)
                if product:
                    print(f"{product['id']:<5} | {product['name']:<25} | {discount:<10}")
                else:
                    print(f"Product with ID {product_id} not found.")

    def remove_discount(self):
        """Removes a discount from a product or all products."""
        print("\nRemove Discount:")
        choice = input("1. Remove discount from a single product\n2. Remove discount from all products\nEnter your choice: ")

        if choice == "1":
            product_id = input("Enter product ID to remove discount: ")
            if product_id in self.discounts:
                del self.discounts[product_id]
                print(f"Discount removed from product ID {product_id}.")
            else:
                print("No discount found for this product.")

        elif choice == "2":
            # Remove all discounts
            self.discounts.clear()
            print("All discounts have been removed from all products.")

        else:
            print("Invalid choice. Please try again.")

    def complete_transaction(self):
        """Completes a transaction and generates a receipt."""
        product_ids = input("Enter product IDs (comma-separated): ")
        product_ids = [pid.strip() for pid in product_ids.split(",")]
        total = 0
        receipt = "\nReceipt:\n"
        invalid_ids = []  # To track invalid product IDs
        valid_product_ids = []  # To track valid product IDs for the report and sales log

        for pid in product_ids:
            product = next((p for p in self.products if p['id'] == pid), None)
            if product:
                price = product['price']
                if pid in self.discounts:
                    price -= price * (self.discounts[pid] / 100)
                total += price
                receipt += f"{product['name']}: RM{price:.2f}\n"
                valid_product_ids.append(pid)  # Only add valid product IDs to the valid list
            else:
                invalid_ids.append(pid)

        # Handle invalid product IDs
        if invalid_ids:
            print(f"\nInvalid Product IDs: {', '.join(invalid_ids)}")
            print("Please ensure all product IDs are correct.")

        receipt += f"Total: RM{total:.2f}\n"
        print(receipt)

        # Log sale for reporting if there were valid items
        if total > 0:
            self.sales.append({"products": valid_product_ids, "total": total})  # Use only valid IDs
        return receipt

    def generate_report(self):
        """Generates a basic sales report."""
        report = "\nSales Report:\n"
        total_sales = sum(sale["total"] for sale in self.sales)
        product_popularity = {p['id']: 0 for p in self.products}

        for sale in self.sales:
            for pid in sale["products"]:
                product_popularity[pid] += 1

        report += f"Total Sales: RM{total_sales:.2f}\n"
        report += "Product Popularity:\n"

        for product in self.products:
            report += f"{product['name']}: {product_popularity[product['id']]} sold\n"

        print(report)
        return report


# Main Menu
def main():
    cashier = CashierSystem("defaultproducts.json")

    print("Welcome to the Cashier System. Products are loaded from 'defaultproducts.json'.")

    while True:
        print("\nMenu:")
        print("1. Add Product")
        print("2. Display Products")
        print("3. Filter Products by Category")
        print("4. Add/Remove Discounts")
        print("5. Complete Transaction")
        print("6. Generate Report")
        print("7. View All Active Discounts")
        print("8. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            cashier.add_product()
        elif choice == "2":
            cashier.display_products()
        elif choice == "3":
            cashier.filter_products_by_category()
        elif choice == "4":
            sub_choice = input("1 to Add Discount, 2 to Remove Discount: ")
            if sub_choice == "1":
                cashier.add_discount()
            elif sub_choice == "2":
                cashier.remove_discount()
            else:
                print("Invalid option.")
        elif choice == "5":
            cashier.complete_transaction()
        elif choice == "6":
            cashier.generate_report()
        elif choice == "7":
            cashier.view_active_discounts()  # Added new option for viewing active discounts
        elif choice == "8":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    main()
