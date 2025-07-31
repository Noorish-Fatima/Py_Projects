import csv
import json
import os
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

EXPENSE_FILE = "expenses.json"

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
# Export to csv
def export_to_csv():
    if not expenses:
        print("No expenses to export")
        return
    filename = input("Enter filename (default: expenses.csv): ")
    if not filename:
        filename = "expenses.csv"
    
    try:
        with open(filename, mode='w', newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["date", "category", "amount"])
            writer.writeheader()
            for expense in expenses:
                writer.writerow(expense)
            print(f"Exported to {filename}")
    except Exception as e:
        print("Failed to Export: ", e)
# Import from csv
def import_from_csv():
    filename = input("Enter csv File to import (default: expenses.csv): ")
    if not filename:
        filename = "expenses.csv"
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            imported = 0
            for row in reader:
                expense = {
                    "date": row["date"],
                    "category": row["category"],
                    "amount": float(row["amount"])
                }
                expenses.append(expense)
                imported+=1
            print(f"Imported {imported} expenses from {filename}")
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print("Failed to Import: ", e)
# Plot monthly Charts
def plot_monthly_charts():
    if not expenses:
        print("No data to plot")
        return 
    # Group by month
    monthly_totals = defaultdict(float)
    for e in expenses:
        month = e['date'][:7]
        monthly_totals[month] += e['amount']
    months = sorted(monthly_totals.keys())
    totals = [monthly_totals[m] for m in months]

    plt.figure(figsize=(8, 4))
    plt.plot(months, totals, marker='o', linestyle='-', color='purple')
    plt.title("Monthly Expenses Chart")
    plt.xlabel('Month')
    plt.ylabel("Toatl spent (RS)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

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
    print(f"\n Total spent: Rs {total:.2f}\n")
# Show filtered data
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
        print("5. Export to csv")
        print("6. Import from csv")
        print("7. Show Total Spent")
        print("8. Plot Monthly Chart")
        print("9. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            show_expenses()
        elif choice == "3":
            filter_by_month()
        elif choice == "4":
            filter_by_category()
        elif choice == "5":
            export_to_csv()
        elif choice == "6":
            import_from_csv()
        elif choice == '7':
            show_total()
        elif choice == '8':
            plot_monthly_charts()
        elif choice == "9":
            break
        else:
            print("Invalid choice. Try again.\n")

# Start app
expenses = load_expenses()
menu()
