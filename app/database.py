import sqlite3
from datetime import datetime


# ---------------------------------
# Database Configuration
# ---------------------------------

DATABASE_NAME = "finance.db"


# ---------------------------------
# Connect To Database
# ---------------------------------

def get_connection():
    return sqlite3.connect(DATABASE_NAME)


# ---------------------------------
# Create Database Tables
# ---------------------------------

def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    # Income table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # Expense table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # Budget table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            month TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ---------------------------------
# Add Income
# ---------------------------------

def save_income(source, amount, date=None):

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO income (source, amount, date)
        VALUES (?, ?, ?)
    """, (source, amount, date))

    connection.commit()
    connection.close()


# ---------------------------------
# Add Expense
# ---------------------------------

def save_expense(category, amount, date=None):

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses (category, amount, date)
        VALUES (?, ?, ?)
    """, (category, amount, date))

    connection.commit()
    connection.close()


# ---------------------------------
# Get All Income
# ---------------------------------

def get_all_income():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, source, amount, date
        FROM income
        ORDER BY date DESC, id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


# ---------------------------------
# Get All Expenses
# ---------------------------------

def get_all_expenses():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, category, amount, date
        FROM expenses
        ORDER BY date DESC, id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


# ---------------------------------
# Get Monthly Income
# ---------------------------------

def get_monthly_income(year, month):

    connection = get_connection()
    cursor = connection.cursor()

    month_text = f"{year:04d}-{month:02d}"

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM income
        WHERE date LIKE ?
    """, (month_text + "%",))

    total = cursor.fetchone()[0]

    connection.close()

    return total


# ---------------------------------
# Get Monthly Expenses
# ---------------------------------

def get_monthly_expenses(year, month):

    connection = get_connection()
    cursor = connection.cursor()

    month_text = f"{year:04d}-{month:02d}"

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE date LIKE ?
    """, (month_text + "%",))

    total = cursor.fetchone()[0]

    connection.close()

    return total


# ---------------------------------
# Get Monthly History
# ---------------------------------

def get_monthly_history():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            strftime('%Y-%m', date) AS month,
            SUM(amount) AS total
        FROM income
        GROUP BY month
        ORDER BY month DESC
    """)

    income_rows = cursor.fetchall()

    cursor.execute("""
        SELECT
            strftime('%Y-%m', date) AS month,
            SUM(amount) AS total
        FROM expenses
        GROUP BY month
        ORDER BY month DESC
    """)

    expense_rows = cursor.fetchall()

    connection.close()

    income_data = {}
    expense_data = {}

    for month, total in income_rows:
        income_data[month] = total

    for month, total in expense_rows:
        expense_data[month] = total

    all_months = set(income_data.keys()) | set(
        expense_data.keys()
    )

    history = []

    for month in sorted(all_months, reverse=True):

        income = income_data.get(month, 0)
        expenses = expense_data.get(month, 0)

        balance = income - expenses

        if income > 0:
            savings_rate = (
                balance / income
            ) * 100
        else:
            savings_rate = 0

        history.append({
            "month": month,
            "income": income,
            "expenses": expenses,
            "balance": balance,
            "savings_rate": savings_rate
        })

    return history


# ---------------------------------
# Save Budget
# ---------------------------------

def save_budget(category, amount, month):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO budgets (category, amount, month)
        VALUES (?, ?, ?)
    """, (category, amount, month))

    connection.commit()
    connection.close()


# ---------------------------------
# Get Budgets
# ---------------------------------

def get_budgets(month=None):

    connection = get_connection()
    cursor = connection.cursor()

    if month is not None:

        cursor.execute("""
            SELECT id, category, amount, month
            FROM budgets
            WHERE month = ?
            ORDER BY category
        """, (month,))

    else:

        cursor.execute("""
            SELECT id, category, amount, month
            FROM budgets
            ORDER BY month DESC, category
        """)

    rows = cursor.fetchall()

    connection.close()

    return rows


# ---------------------------------
# Delete Budget
# ---------------------------------

def delete_budget(budget_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM budgets
        WHERE id = ?
    """, (budget_id,))

    connection.commit()
    connection.close()


# ---------------------------------
# Delete Income
# ---------------------------------

def delete_income(income_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM income
        WHERE id = ?
    """, (income_id,))

    connection.commit()
    connection.close()


# ---------------------------------
# Delete Expense
# ---------------------------------

def delete_expense(expense_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (expense_id,))

    connection.commit()
    connection.close()


# ---------------------------------
# Initialize Database
# ---------------------------------

create_tables()