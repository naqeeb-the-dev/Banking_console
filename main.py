import os
import datetime

# Function to validate account number
def validate_account_number(account_number):
    """
    Validates the given account number.

    Parameters:
    account_number (str): The account number to be validated.

    Returns:
    bool: True if the account number is valid, False otherwise.
    """
    if not account_number.isdigit():
        return False
    if len(account_number) != 10:
        return False
    return True

# Function to validate amount
def validate_amount(amount):
    """
    Validates the given amount.

    Parameters:
    amount (float or str): The amount to be validated.

    Returns:
    bool: True if the amount is valid, False otherwise.
    """
    try:
        amount = float(amount)
        if amount <= 0:
            return False
        return True
    except ValueError:
        return False

# Function to validate date format
def validate_date(date_string):
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Function to generate unique account number
def generate_account_number():
    if os.path.exists("account_numbers.txt"):
        with open("account_numbers.txt", "r") as file:
            lines = file.readlines()
            if lines:
                last_account_number = int(lines[-1])
                new_account_number = last_account_number + 1
            else:
                new_account_number = 1000000001
    else:
        new_account_number = 1000000001

    with open("account_numbers.txt", "a") as file:
        file.write(str(new_account_number) + "\n")

    return str(new_account_number)

# Function to create customer account
def create_customer_account():
    name = input("Enter customer name: ")
    account_type = input("Enter account type (Savings/Current): ").lower()
    while account_type not in ['savings', 'current']:
        account_type = input("Invalid account type. Enter 'Savings' or 'Current': ").lower()
    balance = input("Enter initial balance: ")
    while not validate_amount(balance):
        balance = input("Invalid amount. Enter a valid amount: ")
    password = input("Enter password: ")  # Added password entry

    # Generate unique account number
    account_numbers = [int(line.split(",")[0]) for line in open("customer_accounts.txt").readlines()]
    if account_numbers:
        account_number = max(account_numbers) + 1
    else:
        account_number = 1

    with open("customer_accounts.txt", "a") as file:
        file.write(f"{account_number},{name},{account_type},{balance},{password}\n")

    print(f"Customer registered successfully with account number: {account_number}")

# Function for customer login
def customer_login():
    account_number = input("Enter account number: ")
    password = input("Enter password: ")

    with open("customer_accounts.txt", "r") as file:
        for line in file:
            acc_num, name, acc_type, balance, pwd = line.strip().split(",")
            if acc_num == account_number and pwd == password:
                return acc_num, name, acc_type, float(balance)
    return None

# Function for customer deposit
def customer_deposit(account_number):
    amount = input("Enter deposit amount: ")
    while not validate_amount(amount):
        amount = input("Invalid amount. Enter a valid amount: ")

    with open("customer_accounts.txt", "r") as file:
        lines = file.readlines()

    with open("customer_accounts.txt", "w") as file:
        for line in lines:
            acc_num, name, acc_type, balance, pwd = line.strip().split(",")
            if acc_num == account_number:
                balance = str(float(balance) + float(amount))
            file.write(f"{acc_num},{name},{acc_type},{balance},{pwd}\n")

    # Record transaction in transactions.txt
    with open("transactions.txt", "a") as file:
        file.write(f"{account_number},{datetime.datetime.now().strftime('%Y-%m-%d')},Deposit,{amount}\n")

    print("Deposit successful.")

# Function for customer withdrawal
def customer_withdraw(account_number):
    amount = input("Enter withdrawal amount: ")
    while not validate_amount(amount):
        amount = input("Invalid amount. Enter a valid amount: ")

    with open("customer_accounts.txt", "r") as file:
        lines = file.readlines()

    with open("customer_accounts.txt", "w") as file:
        for line in lines:
            acc_num, name, acc_type, balance, pwd = line.strip().split(",")
            if acc_num == account_number:
                if float(balance) - float(amount) < (100 if acc_type == "savings" else 500):
                    print("Insufficient balance.")
                    return
                balance = str(float(balance) - float(amount))
            file.write(f"{acc_num},{name},{acc_type},{balance},{pwd}\n")

    # Record transaction in transactions.txt
    with open("transactions.txt", "a") as file:
        file.write(f"{account_number},{datetime.datetime.now().strftime('%Y-%m-%d')},Withdrawal,{amount}\n")

    print("Withdrawal successful.")

# Function to generate customer statement of account
def generate_statement_of_account(account_number):
    start_date = input("Enter start date (YYYY-MM-DD): ")
    while not validate_date(start_date):
        start_date = input("Invalid date format. Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    while not validate_date(end_date):
        end_date = input("Invalid date format. Enter end date (YYYY-MM-DD): ")

    total_deposits = 0
    total_withdrawals = 0

    with open("transactions.txt", "r") as file:
        for line in file:
            acc_num, transaction_date, transaction_type, amount = line.strip().split(",")
            if acc_num == account_number and start_date <= transaction_date <= end_date:
                if transaction_type == "Deposit":
                    total_deposits += float(amount)
                else:
                    total_withdrawals += float(amount)

    print(f"Total Deposits: RM {total_deposits}")
    print(f"Total Withdrawals: RM {total_withdrawals}")

# Function for admin staff to update customer details
def admin_update_customer_details():
    account_number = input("Enter customer account number: ")

    with open("customer_accounts.txt", "r") as file:
        lines = file.readlines()

    found = False
    with open("customer_accounts.txt", "w") as file:
        for line in lines:
            acc_num, name, acc_type, balance, pwd = line.strip().split(",")
            if acc_num == account_number:
                print("Customer found. Enter new details.")
                new_name = input(f"Enter new name for customer {name}: ")
                new_account_type = input(f"Enter new account type for customer {name} (Savings/Current): ").lower()
                while new_account_type not in ['savings', 'current']:
                    new_account_type = input("Invalid account type. Enter 'Savings' or 'Current': ").lower()
                new_balance = input(f"Enter new balance for customer {name}: ")
                while not validate_amount(new_balance):
                    new_balance = input("Invalid amount. Enter a valid amount: ")
                file.write(f"{account_number},{new_name},{new_account_type},{new_balance},{pwd}\n")
                found = True
            else:
                file.write(line)

    if not found:
        print("Customer not found.")

# Function to create new admin account
def create_admin_account():
    admin_id = input("Enter admin ID: ")
    admin_password = input("Enter admin password: ")

    with open("admin_accounts.txt", "a") as file:
        file.write(f"{admin_id},{admin_password}\n")

    print("Admin account created successfully.")

# Function for admin staff login
def admin_login():
    admin_id = input("Enter admin ID: ")
    admin_password = input("Enter admin password: ")

    with open("admin_accounts.txt", "r") as file:
        for line in file:
            stored_admin_id, stored_admin_password = line.strip().split(",")
            if admin_id == stored_admin_id and admin_password == stored_admin_password:
                return True
    return False

# Main function
def main():
    super_user_id = "admin"
    super_user_password = "password"

    while True:
        print("\n===== Banking Service Application =====")
        print("1. Customer Registration")
        print("2. Customer Login")
        print("3. Admin Staff Login")
        print("4. Super User Login")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_customer_account()
        elif choice == "2":
            account_info = customer_login()
            if account_info:
                account_number, name, account_type, balance = account_info
                print(f"Welcome, {name} ({account_number})")
                while True:
                    print("\n===== Customer Menu =====")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Generate Statement of Account")
                    print("4. Logout")
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == "1":
                        customer_deposit(account_number)
                    elif sub_choice == "2":
                        customer_withdraw(account_number)
                    elif sub_choice == "3":
                        generate_statement_of_account(account_number)
                    elif sub_choice == "4":
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == "3":
            if admin_login():
                print("Admin Staff Login successful.")
                while True:
                    print("\n===== Admin Staff Menu =====")
                    print("1. Update Customer Details")
                    print("2. Logout")
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == "1":
                        admin_update_customer_details()
                    elif sub_choice == "2":
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Invalid admin ID or password.")
        elif choice == "4":
            super_user_id_input = input("Enter Super User ID: ")
            super_user_password_input = input("Enter Super User Password: ")
            if super_user_id_input == super_user_id and super_user_password_input == super_user_password:
                print("Super User Login successful.")
                while True:
                    print("\n===== Super User Menu =====")
                    print("1. Create New Admin Account")
                    print("2. Logout")
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == "1":
                        create_admin_account()
                    elif sub_choice == "2":
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Invalid Super User ID or password.")
        elif choice == "5":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
