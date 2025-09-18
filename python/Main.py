import random
import string #is mean text, which can combine with letters, numbers, and symbols.

# Global variables
cart = []  # Cart for storing selected items

# Generate a unique 8-character Order ID
def generate_order_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))  #provided by Python, is mean uppercase letters

# 1. Customer Menu
def customer_menu():
    print("Welcome to our Customer System")

    while True:
        print("\nCustomer Menu")  # \n it is used to go next line
        print("1.Manage Account")
        print("2.Product Browsing")
        print("3.Cart Management")
        print("4.Order Tracking")
        print("5.Dish Review")
        print("6.Exit")

        choice = input("Choose an option (1-6): ")
        if choice == '1':
            manage_account()
        elif choice == '2':
            product_browsing()
        elif choice == '3':
            cart_management()
        elif choice == '4':
            order_tracking()
        elif choice == '5':
            dish_review()
        elif choice == '6':
            print("Exiting Customer Menu. ")
            break                                    #To exit the loop
        else:                                        #else is used to ensure that when the user enters an option beyond the range of "1-6", the program will not crash  but will give a prompt and let the user re-select.
            print("Invalid choice. Please try again.")

# 2.Manage Account
def manage_account():
    while True:
        print("\n Manage Account")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option (1-3): ")
        if choice == "1":
            create_account()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Exiting Manage Account. ")
            break
        else:
            print("Invalid choice. Please try again.")

def create_account():
    print("\n--- Create Account ---")
    username = input("Enter username: ").strip() #is used to remove leading and trailing spaces to ensure accurate input
    password = input("Enter password: ").strip()

    if not username or not password:
        print("Username and password cannot be empty. Please try again.")
        return

    with open("Customers.txt", "a") as file:
        file.write(f"{username},{password}\n")
    print("Account created successfully.")


def login():
    print("\n--- Login ---")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    try:
        with open("Customers.txt", "r") as file:
            accounts = file.readlines()
            for account in accounts:
                if ',' not in account or not account.strip():
                    continue
                saved_username, saved_password = account.strip().split(",", 1) #The 1 in split(",", 1) means splitting only once
                if username == saved_username:
                    if password == saved_password:
                        print("Login successful!")
                        return
                    else:
                        print("Incorrect password. Please try again.")
                        return
            print("Username not found. Please create an account first.")
    except FileNotFoundError:
        print("No accounts found. Please create an account first.")


# 3. Product Browsing
def product_browsing():
    print("\nProduct Menu")
    try:
        with open("Product Menu.txt", "r") as file: #"r" mean is just read, cannot modify
            products = file.readlines()
            if products:
                print("Available Products:")
                for product in products:
                     print(product.strip())
            else:
                     print("No products available.")

    except FileNotFoundError:
       print("Product menu file not found. Please contact support.")

# 4. Cart Management
valid_item_codes = [
    "B01", "B02", "B03", "B04", "B05", "B06", "B07",
    "F01", "F02", "F03",
    "P01", "P02", "P03", "P04", "P05", "P06"
]

def cart_management():
    print("\nCart Management")
    while True:
        print("1.Add Item")
        print("2.Remove Item")
        print("3.View Cart")
        print("4.Checkout")
        print("5.Exit Cart Management")

        choice = input("Choose an option (1-5): ")
        if choice == '1':
            item = input("Enter item code to add: ").strip()
            if not item:
                print("Item code cannot be empty.")
            elif item in cart:
                print(f"'{item}' is already in the cart.")
            elif item not in valid_item_codes:
                print(f"'{item}' is an invalid item code. Please enter a valid code.")
            else:
                cart.append(item)
                print(f"'{item}' has been added to the cart.")
        elif choice == '2':
            item = input("Enter item code to remove: ").strip()
            if item in cart:
                cart.remove(item)
                print(f"'{item}' has been removed from the cart.")
            else:
                print("Item is not in the cart.")
        elif choice == '3':
            print("\nYour Cart:", cart if cart else "Cart is empty.")
        elif choice == '4':
           if cart:
               checkout()
               break
           else:
                print("Your Cart is empty,Pls add items before checking out.")
                break
        elif choice == '5':
            print("Exiting Cart Management.")
            break
        else:
            print("Invalid choice. Please try again.")

#Checkout: Save order details
def checkout():
    customer_name = input("Enter your name: ").strip()
    order_id = generate_order_id()

    try:
        with open("Order.txt", "a") as file:
            file.write(f"{order_id} | {customer_name} | {', '.join(cart)} | Pending\n")
        print(f"Order placed successfully! Your Order ID is: {order_id}")
    except Exception as e:
        print(f"Failed to save the order: {e}")
    cart.clear()  # Clear the cart after checkout

# 5. Order Tracking
def order_tracking():
    print("\nOrder Tracking")
    order_id = input("Enter your Order ID to track: ").strip()
    try:
        with open("Order.txt", "r") as file:
            orders = file.readlines()
            for line in orders:
                if line.startswith(order_id):  #Is to check whether the user starts with order id
                    print(f"Order Details: {line.strip()}")
                    return
        print("Order not found. Please check your Order ID.")
    except FileNotFoundError:
        print("Order file not found. Please contact support.")


# 6. Dish Review
def dish_review():
    print("\nDish Review")
    username = input("Enter your username: ").strip()
    dish = input("Enter your dish name: ").strip()
    review = input("Enter your feedback: ").strip()

    with open("Feedback.txt", "a") as file:
        file.write(f"{username},{dish},{review}\n")
    print("Thank you for your feedback :)")


# Run
if __name__ == "__main__":
   customer_menu()
