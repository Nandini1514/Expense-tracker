import re
import os
from datetime import datetime

class Expense:
    # Optional predefined categories (can be expanded or ignored)
    predefined_categories = ["Food", "Transport", "Utilities", "Groceries", "Entertainment"]

    def __init__(self, amount, category, date):
        # Validate amount
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount must be a positive number.")
        self.amount = float(amount)
        
        # Category: Allow any string, but strip whitespace
        self.category = category.strip()
        if not self.category:
            raise ValueError("Category cannot be empty.")
        
        # Validate date format and basic validity
        if not self._is_valid_date(date):
            raise ValueError("Invalid date format. Please use YYYY-MM-DD and ensure it's a valid date.")
        self.date = date

    def _is_valid_date(self, date_str):
        # Check format with regex
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(pattern, date_str):
            return False
        # Check if it's a real date (e.g., no Feb 30)
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def __str__(self):
        # Format for file storage: amount,category,date
        return f"{self.amount:.2f},{self.category},{self.date}"

    @classmethod
    def from_string(cls, s):
        # Deserialize from file string
        parts = s.strip().split(',')
        if len(parts) != 3:
            raise ValueError("Invalid expense format in file.")
        try:
            amount = float(parts[0])
            category = parts[1]
            date = parts[2]
            return cls(amount, category, date)
        except (ValueError, IndexError):
            raise ValueError("Invalid expense data in file.")

def save_expense(expense):
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    # Append to file using context manager
    with open('data/expenses.txt', 'a') as f:
        f.write(str(expense) + '\n')

def load_expenses():
    expenses = []
    try:
        with open('data/expenses.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line:  # Skip empty lines
                    try:
                        exp = Expense.from_string(line)
                        expenses.append(exp)
                    except ValueError:
                        # Skip invalid lines but continue loading others
                        pass
    except FileNotFoundError:
        # File doesn't exist yet; return empty list
        pass
    return expenses

def summarize_by_category(expenses):
    # Use a dictionary to group and sum by category
    summary = {}
    for exp in expenses:
        if exp.category in summary:
            summary[exp.category] += exp.amount
        else:
            summary[exp.category] = exp.amount
    return summary

def main():
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Summarize by Category")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            summarize_expenses()
        elif choice == '4':
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def add_expense():
    try:
        amount_input = input("Enter amount: ").strip()
        if not amount_input:
            raise ValueError("Amount cannot be empty.")
        amount = float(amount_input)
        
        category = input("Enter category: ").strip()
        
        date = input("Enter date (YYYY-MM-DD): ").strip()
        
        exp = Expense(amount, category, date)
        save_expense(exp)
        print("Expense added successfully!")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def view_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return
    
    # Display in a tabulated format
    print(f"{'Amount':<10} {'Category':<15} {'Date':<12}")
    print("-" * 40)
    for exp in expenses:
        print(f"{exp.amount:<10.2f} {exp.category:<15} {exp.date:<12}")

def summarize_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses to summarize.")
        return
    
    summary = summarize_by_category(expenses)
    print(f"{'Category':<15} {'Total Amount':<12}")
    print("-" * 30)
    for cat, total in summary.items():
        print(f"{cat:<15} {total:<12.2f}")

if __name__ == "__main__":
    main()