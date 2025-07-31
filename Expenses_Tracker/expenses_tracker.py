import csv
import sqlite3
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

DB_FILE = "expenses.db"

# Connect to SQLite DB
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Creating  table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL
)
""")
conn.commit()

# Add a new expense
def add_expense():
    date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    category = input("Enter category (food, transport, bills, etc.): ").strip()
    amount = float(input("Enter amount: "))

    cursor.execute("INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)", (date, category, amount))
    conn.commit()
    print("Expense added!\n")

# Export to csv
def export_to_csv():
    cursor.execute("SELECT date, category, amount FROM expenses")
    rows = cursor.fetchall()

    if not rows:
        print("No expenses to export")
        return

    filename = input("Enter filename (default: expenses.csv): ")
    if not filename:
        filename = "expenses.csv"

    try:
        with open(filename, mode='w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "category", "amount"])
            writer.writerows(rows)
            print(f"Exported to {filename}")
    except Exception as e:
        print("Failed to Export: ", e)

# Import from csv
def import_from_csv():
    filename = input("Enter csv file to import (default: expenses.csv): ")
    if not filename:
        filename = "expenses.csv"
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            imported = 0
            for row in reader:
                cursor.execute("INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)",
                               (row["date"], row["category"], float(row["amount"])))
                imported += 1
            conn.commit()
            print(f"Imported {imported} expenses from {filename}")
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print("Failed to Import: ", e)

# Plot monthly chart
def plot_monthly_charts():
    cursor.execute("SELECT date, amount FROM expenses")
    rows = cursor.fetchall()
    if not rows:
        print("No data to plot")
        return

    monthly_totals = defaultdict(float)
    for date, amount in rows:
        month = date[:7]
        monthly_totals[month] += amount

    months = sorted(monthly_totals.keys())
    totals = [monthly_totals[m] for m in months]

    plt.figure(figsize=(8, 4))
    plt.plot(months, totals, marker='o', linestyle='-', color='purple')
    plt.title("Monthly Expenses Chart")
    plt.xlabel('Month')
    plt.ylabel("Total spent (Rs)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Show all expenses
def show_expenses():
    cursor.execute("SELECT date, category, amount FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    if not rows:
        print("No expenses recorded.\n")
        return

    print("\n All Expenses:")
    for i, exp in enumerate(rows, 1):
        print(f"{i}. {exp[0]} | {exp[1]} | Rs {exp[2]:.2f}")
    print()

# Show total spent
def show_total():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0
    print(f"\n Total spent: Rs {total:.2f}\n")

# Filtered data
def show_expenses_filtered(filtered_rows):
    if not filtered_rows:
        print("No expenses to show.")
        return
    for row in filtered_rows:
        print(f"{row[0]} | {row[1]} | Rs {row[2]:.2f}")

# Filter by month
def filter_by_month():
    month = input('Enter Month (MM): ')
    year = input('Enter Year (YYYY): ')
    cursor.execute("SELECT date, category, amount FROM expenses WHERE strftime('%Y-%m', date) = ?", (f"{year}-{month}",))
    rows = cursor.fetchall()
    show_expenses_filtered(rows)

# Filter by category
def filter_by_category():
    category = input("Enter category to filter: ").lower()
    cursor.execute("SELECT date, category, amount FROM expenses WHERE lower(category) = ?", (category,))
    rows = cursor.fetchall()
    show_expenses_filtered(rows)

# Menu 
def menu():
    while True:
        print("=== Expense Tracker ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Filter by Month")
        print("4. Filter by Category")
        print("5. Export to CSV")
        print("6. Import from CSV")
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

# Start the app
menu()

# Close DB on exit
conn.close()

