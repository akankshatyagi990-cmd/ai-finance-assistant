def calculate_financial_summary(total_income, total_expenses):
    remaining_balance = total_income - total_expenses

    if total_income > 0:
        savings_percentage = (
            remaining_balance / total_income
        ) * 100
    else:
        savings_percentage = 0

    return remaining_balance, savings_percentage


def find_highest_spending_category(expenses):

    if len(expenses) == 0:
        return None, 0

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

    highest_category = max(
        category_totals,
        key=category_totals.get
    )

    highest_amount = category_totals[highest_category]

    return highest_category, highest_amount


def show_financial_summary(
    total_income,
    total_expenses,
    expenses
):

    remaining_balance, savings_percentage = (
        calculate_financial_summary(
            total_income,
            total_expenses
        )
    )

    highest_category, highest_amount = (
        find_highest_spending_category(expenses)
    )

    print("\n=================================")
    print("       Financial Summary")
    print("=================================")

    print(
        "Total Income:",
        round(total_income, 2)
    )

    print(
        "Total Expenses:",
        round(total_expenses, 2)
    )

    print("-------------------------------")

    print(
        "Remaining Balance:",
        round(remaining_balance, 2)
    )

    print(
        "Savings Percentage:",
        round(savings_percentage, 2),
        "%"
    )

    if highest_category is not None:

        print(
            "Highest Spending Category:",
            highest_category
        )

        print(
            "Highest Spending Amount:",
            round(highest_amount, 2)
        )

    else:

        print(
            "Highest Spending Category: "
            "No expenses recorded."
        )

    print("-------------------------------")

    if remaining_balance > 0:

        print(
            "Financial Status: "
            "You have money left."
        )

    elif remaining_balance == 0:

        print(
            "Financial Status: "
            "Income and expenses are equal."
        )

    else:

        print(
            "Financial Status: "
            "Expenses are higher than income."
        )