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

def show_expenses_filtered(data):
    if not data:
        print("No expenses to show.")
        return
    for e in data:
        print(f"{e['date']} | {e['category']} | ${e['amount']}")
# Filter by month
def filter_by_month():
    month = input('Enter Month (MM): ')
    year = input('Enter Year (YYYY)')
    filtered = [e for e in expenses if e['date'].startswith(f"{year}-{month}")]
    show_expenses_filtered(filtered)
# Filter by Category
def filter_by_category():
    category = input("Enter category to filter: ").lower()
    filtered = [e for e in expenses if e['category'].lower()== category]
    show_expenses_filtered(filtered)
# menu
def menu():
    while True:
        print("=== Expense Tracker ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Filter by Month")
        print("4. Filter by Category")
        print("5. Show Total Spent")
        print("6. Exit")

        choice = input("Select an option (1-4): ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            show_expenses()
        elif choice == "3":
            filter_by_month()
        elif choice == "4":
            filter_by_category()
        elif choice == '5':
            show_total()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Try again.\n")

# Start app
expenses = load_expenses()
menu()
