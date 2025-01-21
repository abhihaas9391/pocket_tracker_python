import tkinter as tk
from tkinter import messagebox, ttk
import pickle
import pathlib
import matplotlib.pyplot as plt
from datetime import datetime


class Transaction:
    def __init__(self, trans_id, date, amount, category, type_):
        self.trans_id = trans_id
        self.date = date
        self.amount = amount
        self.category = category
        self.type = type_  # 'income' or 'expense'


class FinanceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tracker Demo")
        self.root.geometry("600x600")
        self.root.configure(bg="#f4f4f9")

        self.transactions = []
        self.categories = ['Salary', 'Groceries', 'Bills', 'Entertainment', 'Miscellaneous']
        self.budget = 0
        self.load_data()

        self.create_main_menu()

    def create_main_menu(self):
        tk.Label(
            self.root, text="Finance Tracker", font=("Helvetica", 24, "bold"), bg="#f4f4f9", fg="#333"
        ).pack(pady=10)

        buttons_frame = tk.Frame(self.root, bg="#f4f4f9")
        buttons_frame.pack(pady=20)

        buttons = [
            ("Add Income", self.add_income),
            ("Add Expense", self.add_expense),
            ("Set Budget", self.set_budget),
            ("View Summary", self.view_summary),
            ("View Transactions", self.view_transactions),
            ("View Pie Chart", self.view_pie_chart),
            ("Reset Data", self.reset_data),
            ("Exit", self.exit_app),
        ]

        for text, command in buttons:
            tk.Button(
                buttons_frame,
                text=text,
                width=25,
                height=2,
                bg="#6200ea",
                fg="white",
                font=("Helvetica", 12),
                command=command,
            ).pack(pady=5)

    def add_income(self):
        self.transaction_form("income")

    def add_expense(self):
        self.transaction_form("expense")

    def transaction_form(self, trans_type):
        form = tk.Toplevel(self.root)
        form.title(f"Add {trans_type.capitalize()}")
        form.geometry("400x400")
        form.configure(bg="#f4f4f9")

        tk.Label(form, text=f"Add {trans_type.capitalize()}", font=("Helvetica", 16, "bold"), bg="#f4f4f9").pack(pady=10)

        labels = ["Date (YYYY-MM-DD):", "Amount:", "Category:"]
        entries = []

        for i, label in enumerate(labels):
            tk.Label(form, text=label, bg="#f4f4f9", font=("Helvetica", 12)).pack(pady=5)
            entry = tk.Entry(form, font=("Helvetica", 12))
            entry.pack(pady=5)
            entries.append(entry)

        category_combobox = ttk.Combobox(form, values=self.categories, state="readonly", font=("Helvetica", 12))
        category_combobox.set(self.categories[0])
        category_combobox.pack(pady=5)

        def submit():
            try:
                trans_id = len(self.transactions) + 1
                date, amount, _ = [entry.get() for entry in entries]
                category = category_combobox.get()
                amount = float(amount)
                if not date or not category:
                    raise ValueError("All fields are required!")
                self.transactions.append(Transaction(trans_id, date, amount, category, trans_type))
                messagebox.showinfo("Success", f"{trans_type.capitalize()} added successfully!")
                self.save_data()  # Save data after each transaction
                form.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        tk.Button(
            form,
            text="Submit",
            bg="#6200ea",
            fg="white",
            font=("Helvetica", 12),
            command=submit,
        ).pack(pady=20)

    def set_budget(self):
        budget_window = tk.Toplevel(self.root)
        budget_window.title("Set Budget")
        budget_window.geometry("400x200")
        budget_window.configure(bg="#f4f4f9")

        tk.Label(budget_window, text="Set Monthly Budget", font=("Helvetica", 16, "bold"), bg="#f4f4f9").pack(pady=10)
        tk.Label(budget_window, text="Enter Budget Amount:", bg="#f4f4f9", font=("Helvetica", 12)).pack(pady=10)

        budget_entry = tk.Entry(budget_window, font=("Helvetica", 12))
        budget_entry.pack(pady=5)

        def submit_budget():
            try:
                self.budget = float(budget_entry.get())
                messagebox.showinfo("Success", f"Budget set to {self.budget}")
                self.save_data()  # Save data after setting budget
                budget_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input! Please enter a valid number.")

        tk.Button(
            budget_window,
            text="Submit",
            bg="#6200ea",
            fg="white",
            font=("Helvetica", 12),
            command=submit_budget,
        ).pack(pady=20)

    def view_summary(self):
        income = sum(t.amount for t in self.transactions if t.type == "income")
        expenses = sum(t.amount for t in self.transactions if t.type == "expense")
        balance = income - expenses

        summary = (
            f"Total Income: {income}\n"
            f"Total Expenses: {expenses}\n"
            f"Remaining Balance: {balance}\n"
            f"Budget: {self.budget}\n"
        )

        if self.budget > 0:
            if expenses > self.budget:
                summary += f"Warning: You have exceeded your budget by {expenses - self.budget}!\n"
            else:
                summary += f"Good job! You are within your budget by {self.budget - expenses}.\n"

        messagebox.showinfo("Summary", summary)

    def view_transactions(self):
        transactions_window = tk.Toplevel(self.root)
        transactions_window.title("Transactions")
        transactions_window.geometry("500x400")
        transactions_window.configure(bg="#f4f4f9")

        tk.Label(transactions_window, text="All Transactions", font=("Helvetica", 16, "bold"), bg="#f4f4f9").pack(pady=10)

        if not self.transactions:
            tk.Label(transactions_window, text="No transactions found!", font=("Helvetica", 12), bg="#f4f4f9").pack(pady=20)
            return

        columns = ("ID", "Date", "Amount", "Category", "Type")
        tree = ttk.Treeview(transactions_window, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        tree.pack(fill=tk.BOTH, expand=True)

        for t in self.transactions:
            tree.insert("", tk.END, values=(t.trans_id, t.date, t.amount, t.category, t.type.capitalize()))

    def view_pie_chart(self):
        income = sum(t.amount for t in self.transactions if t.type == "income")
        expenses = sum(t.amount for t in self.transactions if t.type == "expense")

        categories = {}
        for t in self.transactions:
            if t.type == 'expense':
                categories[t.category] = categories.get(t.category, 0) + t.amount

        labels = list(categories.keys())
        values = list(categories.values())

        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=["#6200ea", "#ff6f61", "#4caf50", "#ffeb3b", "#ff9800"])
        plt.title("Expense Breakdown")
        plt.axis("equal")
        plt.show()

    def reset_data(self):
        self.transactions = []
        self.budget = 0
        self.save_data()  # Save reset data
        messagebox.showinfo("Reset", "Data has been reset successfully.")

    def exit_app(self):
        self.save_data()
        self.root.destroy()

    def save_data(self):
        """Save the current transactions and budget to a .data file."""
        with open("finance_tracker.data", "wb") as file:
            pickle.dump({"transactions": self.transactions, "budget": self.budget}, file)

    def load_data(self):
        """Load the saved data from the .data file."""
        file = pathlib.Path("finance_tracker.data")
        if file.exists():
            with open("finance_tracker.data", "rb") as file:
                data = pickle.load(file)
                self.transactions = data.get("transactions", [])
                self.budget = data.get("budget", 0)


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTrackerApp(root)
    root.mainloop()
