 simple desktop expense tracking app built using Python Tkinter and SQLite, styled like an Excel spreadsheet. It allows users to add, edit, delete, filter, and visualize expenses easily through a user-friendly interface.

------ Features -----------
- Add Expenses — Add new entries with date, category, and amount.

- Edit & Delete — Modify or remove any existing entry.

- Filters

""" By Month (YYYY-MM)

""" By Category (case-insensitive)

- Monthly Chart — Line chart of total spending per month using Matplotlib.

- Total Spent — One-click total expense calculator.

- CSV Import — Import expenses from .csv file (with headers: date, category, amount).

- CSV Export — Export current records to a .csv file.

- Auto ID & Ordering — Expenses are stored with auto-increment IDs and shown in reverse chronological order.

- Excel-Styled UI — Spreadsheet-like look using ttk.Treeview, alternating row colors, light green headers, and clean layout.

------- Tech Stack ---------
**Frontend: Tkinter GUI
**Backend: SQLite database

**Visualization: Matplotlib

**Data Handling: CSV file import/export