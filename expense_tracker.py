import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Expense:
    def __init__(self, amount, category, description, date=None):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date if date else datetime.now().date()

    def __str__(self):
        return f"{self.date} - {self.category}: ${self.amount:.2f} - {self.description}"

class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.monthly_income = 0.0
        self.savings_goal = 0.0
        self.category_colors = {}
        self.recurring_expenses = []

    def add_expense(self, amount, category, description, date=None):
        self.expenses.append(Expense(amount, category, description, date))

    def edit_expense(self, index, amount, category, description):
        self.expenses[index] = Expense(amount, category, description, self.expenses[index].date)

    def delete_expense(self, index):
        del self.expenses[index]

    def view_expenses(self):
        return self.expenses

    def total_expenses(self):
        return sum(expense.amount for expense in self.expenses)

    def filter_expenses(self, category):
        return [expense for expense in self.expenses if expense.category == category]

    def set_monthly_income(self, income):
        self.monthly_income = income

    def get_daily_budget(self):
        days_in_month = (datetime.now().replace(month=datetime.now().month % 12 + 1, day=1) - timedelta(days=1)).day
        return self.monthly_income / days_in_month if self.monthly_income > 0 else 0

    def set_savings_goal(self, goal):
        self.savings_goal = goal

    def get_savings_progress(self):
        saved_amount = self.monthly_income - self.total_expenses()
        return saved_amount, self.savings_goal

    def set_category_color(self, category, color):
        self.category_colors[category] = color

    def get_category_color(self, category):
        return self.category_colors.get(category, "#FFFFFF")

    def export_expenses(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Category', 'Amount', 'Description'])
            writer.writerows([[expense.date, expense.category, expense.amount, expense.description] for expense in self.expenses])

    def import_expenses(self, filename):
        try:
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                self.expenses = [Expense(float(row[2]), row[1], row[3], datetime.strptime(row[0], '%Y-%m-%d').date()) for row in reader]
        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"File '{filename}' not found.")

    def add_recurring_expense(self, amount, category, description, start_date, frequency_days):
        self.recurring_expenses.append((amount, category, description, start_date, frequency_days))
        self.update_recurring_expenses()

    def update_recurring_expenses(self):
        current_date = datetime.now().date()
        for expense in self.recurring_expenses:
            amount, category, description, start_date, frequency_days = expense
            while start_date <= current_date:
                start_date += timedelta(days=frequency_days)
            while start_date <= datetime.now().date():
                self.expenses.append(Expense(amount, category, description, start_date))
                start_date += timedelta(days=frequency_days)

    def set_reminder(self, reminder_date, message):
        messagebox.showinfo("Reminder Set", f"Reminder set for {reminder_date}: {message}")

class ExpenseTrackerGUI:
    def __init__(self, root):
        self.tracker = ExpenseTracker()
        self.root = root
        self.root.title("Expense Tracker")
        self.password = "password"  # Default password
        self.authenticated = False

        self.authenticate()

    def authenticate(self):
        password = simpledialog.askstring("Password", "Enter Password:", show='*')
        if password == self.password:
            self.authenticated = True
            self.setup_gui()
        else:
            messagebox.showerror("Error", "Incorrect Password!")
            self.root.destroy()

    def setup_gui(self):
        ttk.Style().configure("TButton", padding=10)

        # Create a scrollable frame
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.setup_input_frame()
        self.setup_view_frame()
        self.setup_income_frame()
        self.setup_report_frame()
        self.setup_graph_frame()

        # Centering the scrollable frame contents
        self.center_frame_contents()

    def setup_input_frame(self):
        self.input_frame = ttk.LabelFrame(self.scrollable_frame, text="Add/Edit/Delete Expense", padding="10")
        self.input_frame.pack(padx=10, pady=10)

        ttk.Label(self.input_frame, text="Amount:").grid(row=0, column=0, sticky=tk.W)
        self.amount_var = tk.DoubleVar()
        ttk.Entry(self.input_frame, textvariable=self.amount_var).grid(row=0, column=1, sticky=tk.W)

        ttk.Label(self.input_frame, text="Category:").grid(row=1, column=0, sticky=tk.W)
        self.category_var = tk.StringVar()
        ttk.Entry(self.input_frame, textvariable=self.category_var).grid(row=1, column=1, sticky=tk.W)

        ttk.Label(self.input_frame, text="Description:").grid(row=2, column=0, sticky=tk.W)
        self.description_var = tk.StringVar()
        ttk.Entry(self.input_frame, textvariable=self.description_var).grid(row=2, column=1, sticky=tk.W)

        ttk.Button(self.input_frame, text="Add Expense", command=self.add_expense).grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Button(self.input_frame, text="Edit Expense", command=self.edit_expense).grid(row=3, column=1, sticky=tk.W, pady=5)
        ttk.Button(self.input_frame, text="Delete Expense", command=self.delete_expense).grid(row=3, column=2, sticky=tk.W, pady=5)

    def setup_view_frame(self):
        self.view_frame = ttk.LabelFrame(self.scrollable_frame, text="View Expenses", padding="10")
        self.view_frame.pack(padx=10, pady=10)

        ttk.Label(self.view_frame, text="Filter by Category:").grid(row=0, column=0, sticky=tk.W)
        self.filter_var = tk.StringVar()
        ttk.Entry(self.view_frame, textvariable=self.filter_var).grid(row=0, column=1, sticky=tk.W)
        ttk.Button(self.view_frame, text="Filter", command=self.filter_expenses).grid(row=0, column=2, sticky=tk.W)

        self.expense_listbox = tk.Listbox(self.view_frame, height=10, width=60)
        self.expense_listbox.grid(row=1, column=0, columnspan=3, pady=10)

        ttk.Button(self.view_frame, text="View Expenses", command=self.view_expenses).grid(row=2, column=0, sticky=tk.W)
        ttk.Button(self.view_frame, text="Show Total Expenses", command=self.show_total_expenses).grid(row=2, column=1, sticky=tk.W)

    def setup_income_frame(self):
        self.income_frame = ttk.LabelFrame(self.scrollable_frame, text="Monthly Income and Savings", padding="10")
        self.income_frame.pack(padx=10, pady=10)

        ttk.Label(self.income_frame, text="Monthly Income:").grid(row=0, column=0, sticky=tk.W)
        self.income_var = tk.DoubleVar()
        ttk.Entry(self.income_frame, textvariable=self.income_var).grid(row=0, column=1, sticky=tk.W)
        ttk.Button(self.income_frame, text="Set Income", command=self.set_income).grid(row=0, column=2, sticky=tk.W)

        ttk.Button(self.income_frame, text="Show Daily Budget", command=self.show_daily_budget).grid(row=1, column=0, sticky=tk.W)
        ttk.Button(self.income_frame, text="Set Savings Goal", command=self.set_savings_goal).grid(row=1, column=1, sticky=tk.W)
        ttk.Button(self.income_frame, text="Show Savings Progress", command=self.show_savings_progress).grid(row=1, column=2, sticky=tk.W)

    def setup_report_frame(self):
        self.report_frame = ttk.LabelFrame(self.scrollable_frame, text="Reports", padding="10")
        self.report_frame.pack(padx=10, pady=10)

        ttk.Button(self.report_frame, text="Generate Monthly Report", command=self.generate_monthly_report).pack(anchor="center")

    def setup_graph_frame(self):
        self.graph_frame = ttk.LabelFrame(self.scrollable_frame, text="Expense Graph", padding="10")
        self.graph_frame.pack(padx=10, pady=10)

        ttk.Button(self.graph_frame, text="Show Expense Graph", command=self.show_expense_graph).pack(anchor="center")

    def add_expense(self):
        self.tracker.add_expense(self.amount_var.get(), self.category_var.get(), self.description_var.get())
        self.clear_entries()
        self.view_expenses()

    def edit_expense(self):
        index = self.expense_listbox.curselection()
        if index:
            self.tracker.edit_expense(index[0], self.amount_var.get(), self.category_var.get(), self.description_var.get())
            self.clear_entries()
            self.view_expenses()

    def delete_expense(self):
        index = self.expense_listbox.curselection()
        if index:
            self.tracker.delete_expense(index[0])
            self.view_expenses()

    def view_expenses(self):
        self.expense_listbox.delete(0, tk.END)
        for expense in self.tracker.view_expenses():
            self.expense_listbox.insert(tk.END, str(expense))

    def show_total_expenses(self):
        total_expenses = self.tracker.total_expenses()
        messagebox.showinfo("Total Expenses", f"Total Expenses: ${total_expenses:.2f}")

    def filter_expenses(self):
        category = self.filter_var.get()
        filtered_expenses = self.tracker.filter_expenses(category)
        self.expense_listbox.delete(0, tk.END)
        for expense in filtered_expenses:
            self.expense_listbox.insert(tk.END, str(expense))

    def set_income(self):
        income = self.income_var.get()
        self.tracker.set_monthly_income(income)
        messagebox.showinfo("Income Set", f"Monthly Income set to: ${income:.2f}")

    def show_daily_budget(self):
        daily_budget = self.tracker.get_daily_budget()
        messagebox.showinfo("Daily Budget", f"Daily Budget: ${daily_budget:.2f}")

    def set_savings_goal(self):
        goal = simpledialog.askfloat("Set Savings Goal", "Enter Savings Goal:")
        if goal is not None:
            self.tracker.set_savings_goal(goal)
            messagebox.showinfo("Savings Goal Set", f"Savings Goal set to: ${goal:.2f}")

    def show_savings_progress(self):
        saved_amount, goal = self.tracker.get_savings_progress()
        messagebox.showinfo("Savings Progress", f"Saved: ${saved_amount:.2f} of ${goal:.2f}")

    def generate_monthly_report(self):
        filename = simpledialog.askstring("Generate Monthly Report", "Enter filename to save report:")
        if filename:
            try:
                self.tracker.export_expenses(filename)
                messagebox.showinfo("Report Generated", f"Monthly report saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

    def show_expense_graph(self):
        categories = set(expense.category for expense in self.tracker.expenses)
        colors = [self.tracker.get_category_color(category) for category in categories]
        expenses_by_category = [sum(expense.amount for expense in self.tracker.expenses if expense.category == category) for category in categories]

        plt.clf()
        plt.pie(expenses_by_category, labels=categories, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Expense Distribution by Category')
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def clear_entries(self):
        self.amount_var.set('')
        self.category_var.set('')
        self.description_var.set('')

    def center_frame_contents(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Centering the canvas
        x_offset = max((width - self.canvas.winfo_reqwidth()) // 2, 0)
        y_offset = max((height - self.canvas.winfo_reqheight()) // 2, 0)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=width, height=height)
        self.canvas.xview_moveto(x_offset / width)
        self.canvas.yview_moveto(y_offset / height)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()
