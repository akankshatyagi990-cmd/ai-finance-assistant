def add_expense(expenses, category, amount):
    expense = {
        "category": category,
        "amount": amount
    }

    expenses.append(expense)


def calculate_total_expenses(expenses):
    total = 0

    for expense in expenses:
        total = total + expense["amount"]

    return total


def show_expenses(expenses):
    print("\n--- Expense List ---")

    if len(expenses) == 0:
        print("No expenses recorded.")
        return

    for expense in expenses:
        print(
            expense["category"],
            "₹",
            round(expense["amount"], 2)
        )


def show_category_summary(expenses):
    category_totals = {}

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]

        if category in category_totals:
            category_totals[category] = (
                category_totals[category] + amount
            )
        else:
            category_totals[category] = amount

    print("\n--- Category Summary ---")

    for category, amount in category_totals.items():
        print(category, "₹", round(amount, 2))


def run_expense_tracker():
    expenses = []

    print("\n=================================")
    print("       Expense Tracker")
    print("=================================")

    while True:

        print("\nChoose an option:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Category Summary")
        print("4. View Total Expenses")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            category = input("Enter expense category: ")

            try:
                amount = float(input("Enter expense amount: "))

                if amount <= 0:
                    print("Amount must be greater than 0.")
                else:
                    add_expense(
                        expenses,
                        category,
                        amount
                    )

                    print("Expense added successfully.")

            except ValueError:
                print("Invalid amount. Please enter a number.")

        elif choice == "2":

            show_expenses(expenses)

        elif choice == "3":

            show_category_summary(expenses)

        elif choice == "4":

            total = calculate_total_expenses(expenses)

            print(
                "\nTotal Expenses: ₹",
                round(total, 2)
            )

        elif choice == "5":

            print("\nThank you for using Expense Tracker!")
            break

        else:

            print("Invalid choice. Please select 1 to 5.")


if __name__ == "__main__":
    run_expense_tracker()