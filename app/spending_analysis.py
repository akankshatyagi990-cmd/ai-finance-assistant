def calculate_category_totals(expenses):

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

    return category_totals


def calculate_spending_percentages(
    category_totals,
    total_expenses
):

    category_percentages = {}

    if total_expenses == 0:
        return category_percentages

    for category, amount in category_totals.items():

        percentage = (
            amount / total_expenses
        ) * 100

        category_percentages[category] = percentage

    return category_percentages


def show_spending_analysis(expenses):

    print("\n=================================")
    print("       Spending Analysis")
    print("=================================")

    if len(expenses) == 0:

        print("\nNo expenses recorded.")
        return

    category_totals = calculate_category_totals(
        expenses
    )

    total_expenses = 0

    for amount in category_totals.values():
        total_expenses = total_expenses + amount

    category_percentages = calculate_spending_percentages(
        category_totals,
        total_expenses
    )

    print(
        "\nTotal Expenses: ₹",
        round(total_expenses, 2)
    )

    print("\n--- Spending By Category ---")

    for category in category_totals:

        amount = category_totals[category]
        percentage = category_percentages[category]

        print(
            category,
            "₹",
            round(amount, 2),
            "(",
            round(percentage, 2),
            "%)"
        )

    highest_category = max(
        category_totals,
        key=category_totals.get
    )

    highest_amount = category_totals[
        highest_category
    ]

    print("\n--- Highest Spending ---")

    print(
        "Category:",
        highest_category
    )

    print(
        "Amount: ₹",
        round(highest_amount, 2)
    )

    print("\n--- Recommendation ---")

    highest_percentage = category_percentages[
        highest_category
    ]

    if highest_percentage >= 50:

        print(
            highest_category,
            "accounts for",
            round(highest_percentage, 2),
            "% of your expenses."
        )

        print(
            "Consider reviewing this category "
            "to identify possible savings."
        )

    elif highest_percentage >= 30:

        print(
            highest_category,
            "is a significant part of your "
            "total expenses."
        )

        print(
            "Keep monitoring this category "
            "to control your spending."
        )

    else:

        print(
            "Your spending is distributed "
            "across different categories."
        )

        print(
            "Continue tracking your expenses "
            "to maintain good financial habits."
        )


if __name__ == "__main__":

    sample_expenses = [
        {
            "category": "Rent",
            "amount": 15000
        },
        {
            "category": "Food",
            "amount": 5000
        },
        {
            "category": "Travel",
            "amount": 3000
        },
        {
            "category": "Food",
            "amount": 4000
        }
    ]

    show_spending_analysis(
        sample_expenses
    )