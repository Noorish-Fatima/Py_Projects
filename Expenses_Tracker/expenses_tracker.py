import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
from tkinter import font

# --- Database setup ---
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL
)
""")
conn.commit()

# --- Main app window ---
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("1000x900")
root.configure(bg="#f2f2f2")
root.option_add("*Button.Background", "#898D87")
root.option_add("*Button.ActiveBackground", "#D4EAD3")
root.option_add("*Button.BorderWidth", 1)

# --- Styling ---
style = ttk.Style(root)
style.theme_use("clam")

# Excel-style Treeview
style.configure("Treeview",
    background="white",
    foreground="black",
    rowheight=28,
    fieldbackground="white",
    font=('Calibri', 11)
)
style.configure("Treeview.Heading",
    background="#C3BFBFFF",  # Excel header color
    foreground="black",
    font=('Calibri', 12, 'bold')
)
style.map('Treeview',
    background=[('selected', "#C6D8EF")],
    foreground=[('selected', 'black')]
)

# Default fonts
default_font = font.nametofont("TkDefaultFont")
default_font.configure(family="Calibri", size=11)
root.option_add("*Font", default_font)

style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 10))


# ----- FUNCTIONS -----
def refresh_tree():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT id, date, category, amount FROM expenses ORDER BY date DESC")
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)
    tag_rows()  # Appling zebra striping

def add_expense():
    date = entry_date.get() or datetime.now().strftime("%Y-%m-%d")
    category = entry_category.get()
    try:
        amount = float(entry_amount.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid amount.")
        return
    cursor.execute("INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)",
                   (date, category, amount))
    conn.commit()
    entry_date.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    refresh_tree()
def delete_expense():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select", "Select a row to delete.")
        return
    exp_id = tree.item(selected[0])['values'][0]
    confirm = messagebox.askyesno("Confirm", f"Delete expense #{exp_id}?")
    if confirm:
        cursor.execute("DELETE FROM expenses WHERE id=?", (exp_id,))
        conn.commit()
        refresh_tree()
def edit_expense():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select", "Select a row to edit.")
        return
    item = tree.item(selected[0])
    exp_id, old_date, old_cat, old_amt = item['values']
    def save_changes():
        new_date = e_date.get() or old_date
        new_cat = e_cat.get() or old_cat
        try:
            new_amt = float(e_amt.get()) if e_amt.get() else old_amt
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
            return
        cursor.execute("UPDATE expenses SET date=?, category=?, amount=? WHERE id=?",
                       (new_date, new_cat, new_amt, exp_id))
        conn.commit()
        top.destroy()
        refresh_tree()
    top = tk.Toplevel(root)
    top.title("Edit Expense")
    tk.Label(top, text="Date (YYYY-MM-DD):").pack()
    e_date = tk.Entry(top)
    e_date.insert(0, old_date)
    e_date.pack()
    tk.Label(top, text="Category:").pack()
    e_cat = tk.Entry(top)
    e_cat.insert(0, old_cat)
    e_cat.pack()
    tk.Label(top, text="Amount:").pack()
    e_amt = tk.Entry(top)
    e_amt.insert(0, str(old_amt))
    e_amt.pack()
    tk.Button(top, text="Save Changes", command=save_changes).pack(pady=10)
def show_total():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0
    messagebox.showinfo("Total Spent", f"Total: Rs {total:.2f}")
def filter_by_month():
    def apply_filter():
        m = month.get()
        y = year.get()
        tree.delete(*tree.get_children())
        cursor.execute("SELECT id, date, category, amount FROM expenses WHERE strftime('%Y-%m', date)=?",
                       (f"{y}-{m}",))
        for row in cursor.fetchall():
            tree.insert('', 'end', values=row)
        f.destroy()
    f = tk.Toplevel(root)
    f.title("Filter by Month")
    tk.Label(f, text="Month (MM):").pack()
    month = tk.Entry(f)
    month.pack()
    tk.Label(f, text="Year (YYYY):").pack()
    year = tk.Entry(f)
    year.pack()
    tk.Button(f, text="Apply", command=apply_filter).pack(pady=10)
def filter_by_category():
    def apply_filter():
        c = category.get().lower()
        tree.delete(*tree.get_children())
        cursor.execute("SELECT id, date, category, amount FROM expenses WHERE lower(category)=?", (c,))
        for row in cursor.fetchall():
            tree.insert('', 'end', values=row)
        f.destroy()
    f = tk.Toplevel(root)
    f.title("Filter by Category")
    tk.Label(f, text="Category:").pack()
    category = tk.Entry(f)
    category.pack()
    tk.Button(f, text="Apply", command=apply_filter).pack(pady=10)
def export_csv():
    filename = filedialog.asksaveasfilename(defaultextension=".csv")
    if not filename:
        return
    cursor.execute("SELECT date, category, amount FROM expenses")
    rows = cursor.fetchall()
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "category", "amount"])
            writer.writerows(rows)
        messagebox.showinfo("Success", f"Exported to {filename}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
def import_csv():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not filename:
        return
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                cursor.execute("INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)",
                               (row["date"], row["category"], float(row["amount"])))
                count += 1
            conn.commit()
            refresh_tree()
        messagebox.showinfo("Imported", f"Imported {count} records.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
def plot_chart():
    cursor.execute("SELECT date, amount FROM expenses")
    rows = cursor.fetchall()
    if not rows:
        messagebox.showinfo("Info", "No data to plot.")
        return
    monthly = defaultdict(float)
    for date, amt in rows:
        monthly[date[:7]] += amt
    months = sorted(monthly.keys())
    totals = [monthly[m] for m in months]
    plt.figure(figsize=(8, 4))
    plt.plot(months, totals, marker='o', color='purple')
    plt.title("Monthly Expenses")
    plt.xlabel("Month")
    plt.ylabel("Amount (Rs)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
# ----- UI Layout -----
frame_top = tk.Frame(root)
frame_top.pack(pady=10)
tk.Label(frame_top, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
entry_date = tk.Entry(frame_top)
entry_date.grid(row=0, column=1)
tk.Label(frame_top, text="Category:").grid(row=0, column=2)
entry_category = tk.Entry(frame_top)
entry_category.grid(row=0, column=3)
tk.Label(frame_top, text="Amount:").grid(row=0, column=4)
entry_amount = tk.Entry(frame_top)
entry_amount.grid(row=0, column=5)
tk.Button(frame_top, text="Add Expense", command=add_expense).grid(row=0, column=6, padx=10)
frame_btns = tk.Frame(root)
frame_btns.pack(pady=10)
btns = [
    ("Edit", edit_expense),
    ("Delete", delete_expense),
    ("Filter by Month", filter_by_month),
    ("Filter by Category", filter_by_category),
    ("Show Total", show_total),
    ("Import CSV", import_csv),
    ("Export CSV", export_csv),
    ("Plot Chart", plot_chart),
    ("Refresh", refresh_tree),
]
for i, (text, cmd) in enumerate(btns):
    ttk.Button(frame_btns, text=text, command=cmd).grid(row=0, column=i, padx=4, pady=2)

tree = ttk.Treeview(root, columns=("ID", "Date", "Category", "Amount"), show="headings", selectmode="browse")
for col in ("ID", "Date", "Category", "Amount"):
    tree.heading(col, text=col)
    tree.column(col, anchor="center")
    # Setting column widths and alignments
    tree.column("ID", anchor="center", width=50)
    tree.column("Date", anchor="center", width=100)
    tree.column("Category", anchor="w", width=150)
    tree.column("Amount", anchor="e", width=100)
tree.pack(fill="both", expand=True, padx=15, pady=10)
def tag_rows():
    for i, row in enumerate(tree.get_children()):
        tree.item(row, tags=('evenrow' if i % 2 == 0 else 'oddrow'))

tree.tag_configure('evenrow', background='#F2F2F2')  # Light gray
tree.tag_configure('oddrow', background='white')

refresh_tree()
root.mainloop()
conn.close()


