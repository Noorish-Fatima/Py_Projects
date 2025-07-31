import sqlite3
import csv
import os
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

# Export to CSV
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

# Import from CSV
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
    cursor.execute("SELECT id, date, category, amount FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    if not rows:
        print("No expenses recorded.\n")
        return

    print("\n All Expenses:")
    for exp in rows:
        print(f"{exp[0]}. {exp[1]} | {exp[2]} | Rs {exp[3]:.2f}")
    print()
# edit expenses
def edit_expense():
    show_expenses()
    try:
        exp_id = int(input("Enter the ID of the expense to edit: "))
        cursor.execute("SELECT * FROM expenses WHERE id = ?", (exp_id,))
        row = cursor.fetchone()
        if not row:
            print("Expense not found.")
            return

        new_date = input(f"Enter new date (YYYY-MM-DD) or leave blank to keep [{row[1]}]: ")
        new_category = input(f"Enter new category or leave blank to keep [{row[2]}]: ")
        new_amount = input(f"Enter new amount or leave blank to keep [{row[3]}]: ")

        updated_date = new_date or row[1]
        updated_category = new_category or row[2]
        updated_amount = float(new_amount) if new_amount else row[3]

        cursor.execute("UPDATE expenses SET date = ?, category = ?, amount = ? WHERE id = ?",
                       (updated_date, updated_category, updated_amount, exp_id))
        conn.commit()
        print("Expense updated successfully.\n")
    except ValueError:
        print("Invalid input.\n")
# delete expenses
def delete_expense():
    show_expenses()
    try:
        exp_id = int(input("Enter the ID of the expense to delete: "))
        cursor.execute("SELECT * FROM expenses WHERE id = ?", (exp_id,))
        row = cursor.fetchone()
        if not row:
            print("Expense not found.")
            return

        confirm = input(f"Are you sure you want to delete expense #{exp_id}? (y/n): ").lower()
        if confirm == 'y':
            cursor.execute("DELETE FROM expenses WHERE id = ?", (exp_id,))
            conn.commit()
            print("Expense deleted successfully.\n")
        else:
            print("Deletion cancelled.\n")
    except ValueError:
        print("Invalid input.\n")

# Show total spent
def show_total():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0
    print(f"\n Total spent: Rs {total:.2f}\n")

# Filtered view
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

# Menu loop
def menu():
    while True:
        print("=== Expense Tracker ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Filter by Month")
        print("4. Filter by Category")
        print("5. Export to CSV")
        print("6. Import from CSV")
        print("7. Edit Expenses")
        print("8. Delete Expenses")
        print("9. Show Total Spent")
        print("10. Plot Monthly Chart")
        print("11. Exit")

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
            edit_expense()
        elif choice == '8':
            delete_expense()
        elif choice == '9':
            show_total()
        elif choice == '10':
            plot_monthly_charts()
        elif choice == "11":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")

# Start the app
menu()

# Close DB on exit
conn.close()
