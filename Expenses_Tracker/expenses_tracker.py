import json
import os
from datetime import datetime

EXPENSE_FILE = "Expenses_Tracker/expenses.json"

# Load or initialize expense data
def load_expenses():
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "r") as file:
            return json.load(file)
    return []

def save_expenses(expenses):
    with open(EXPENSE_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

# Add a new expense
def add_expense():
    date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    category = input("Enter category (food, transport, bills, etc.): ").strip()
    amount = float(input("Enter amount: "))

    expense = {
        "date": date,
        "category": category,
        "amount": amount
    }

    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added!\n")

# Show all expenses
def show_expenses():
    if not expenses:
        print("No expenses recorded.\n")
        return

    print("\n All Expenses:")
    for i, exp in enumerate(expenses, 1):
        print(f"{i}. {exp['date']} | {exp['category']} | Rs {exp['amount']:.2f}")
    print()

# Show total spent
def show_total():
    total = sum(exp["amount"] for exp in expenses)
    print(f"\n💸 Total spent: Rs {total:.2f}\n")

# menu
def menu():
    while True:
        print("=== Expense Tracker ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Total Spent")
        print("4. Exit")

        choice = input("Select an option (1-4): ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            show_expenses()
        elif choice == "3":
            show_total()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")

# Start app
expenses = load_expenses()
menu()
