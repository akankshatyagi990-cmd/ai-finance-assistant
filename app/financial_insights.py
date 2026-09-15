def calculate_percentage_change(current, previous):
    """
    Calculate percentage change between two values.
    """

    if previous == 0:

        if current == 0:
            return 0

        return 100

    change = (
        (current - previous)
        / previous
    ) * 100

    return change


def calculate_savings(income, expenses):
    """
    Calculate savings amount and savings percentage.
    """

    savings = income - expenses

    if income > 0:
        savings_percentage = (
            savings / income
        ) * 100
    else:
        savings_percentage = 0

    return savings, savings_percentage


def calculate_expense_ratio(income, expenses):
    """
    Calculate what percentage of income
    is being spent.
    """

    if income <= 0:
        return 0

    expense_ratio = (
        expenses / income
    ) * 100

    return expense_ratio


def calculate_category_totals(expenses):
    """
    Calculate total spending for each category.
    """

    category_totals = {}

    for expense in expenses:

        category = expense["category"]
        amount = expense["amount"]

        if category in category_totals:

            category_totals[category] += amount

        else:

            category_totals[category] = amount

    return category_totals


def find_highest_spending_category(expenses):
    """
    Find the category with the highest spending.
    """

    category_totals = calculate_category_totals(
        expenses
    )

    if len(category_totals) == 0:
        return None, 0

    highest_category = max(
        category_totals,
        key=category_totals.get
    )

    highest_amount = (
        category_totals[highest_category]
    )

    return highest_category, highest_amount


def generate_financial_insights(
    current_income,
    current_expenses,
    previous_income,
    previous_expenses,
    expenses
):
    """
    Generate financial intelligence
    based on current and previous month data.
    """

    current_savings, current_savings_percentage = (
        calculate_savings(
            current_income,
            current_expenses
        )
    )

    previous_savings, previous_savings_percentage = (
        calculate_savings(
            previous_income,
            previous_expenses
        )
    )

    income_change = calculate_percentage_change(
        current_income,
        previous_income
    )

    expense_change = calculate_percentage_change(
        current_expenses,
        previous_expenses
    )

    savings_change = calculate_percentage_change(
        current_savings,
        previous_savings
    )

    expense_ratio = calculate_expense_ratio(
        current_income,
        current_expenses
    )

    highest_category, highest_amount = (
        find_highest_spending_category(
            expenses
        )
    )

    insights = []

    alerts = []

    # Negative balance
    if current_savings < 0:

        alerts.append(
            "Your expenses are higher than your income."
        )

        insights.append(
            "Your current spending is above your income. "
            "Review your major expenses."
        )

    # High expense ratio
    elif expense_ratio >= 70:

        alerts.append(
            "More than 70% of your income is being spent."
        )

        insights.append(
            "Your expense level is relatively high. "
            "Consider reviewing your largest spending categories."
        )

    # Strong savings
    elif current_savings_percentage >= 30:

        insights.append(
            "Your savings rate is strong. "
            "Continue maintaining this financial habit."
        )

    # Low savings
    elif current_income > 0:

        insights.append(
            "Your savings rate could be improved. "
            "Try to reduce unnecessary expenses."
        )

    # Income trend
    if previous_income > 0:

        if income_change > 0:

            insights.append(
                f"Your income increased by "
                f"{income_change:.1f}% compared with the previous month."
            )

        elif income_change < 0:

            alerts.append(
                f"Your income decreased by "
                f"{abs(income_change):.1f}% compared with the previous month."
            )

    # Expense trend
    if previous_expenses > 0:

        if expense_change > 0:

            alerts.append(
                f"Your expenses increased by "
                f"{expense_change:.1f}% compared with the previous month."
            )

        elif expense_change < 0:

            insights.append(
                f"Your expenses decreased by "
                f"{abs(expense_change):.1f}% compared with the previous month."
            )

    # Savings trend
    if previous_savings != 0:

        if savings_change > 0:

            insights.append(
                f"Your savings improved by "
                f"{savings_change:.1f}% compared with the previous month."
            )

        elif savings_change < 0:

            alerts.append(
                f"Your savings decreased by "
                f"{abs(savings_change):.1f}% compared with the previous month."
            )

    # Highest spending category
    if highest_category is not None:

        insights.append(
            f"Your highest spending category is "
            f"{highest_category}, with spending of "
            f"₹{highest_amount:,.2f}."
        )

    return {
        "current_savings": current_savings,
        "current_savings_percentage": current_savings_percentage,
        "income_change": income_change,
        "expense_change": expense_change,
        "savings_change": savings_change,
        "expense_ratio": expense_ratio,
        "highest_category": highest_category,
        "highest_amount": highest_amount,
        "insights": insights,
        "alerts": alerts
    }


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
        }
    ]

    result = generate_financial_insights(
        current_income=60000,
        current_expenses=23000,
        previous_income=55000,
        previous_expenses=25000,
        expenses=sample_expenses
    )

    print("\n=================================")
    print("     Financial Intelligence")
    print("=================================")

    print(
        "\nCurrent Savings: ₹",
        round(
            result["current_savings"],
            2
        )
    )

    print(
        "Savings Rate:",
        round(
            result["current_savings_percentage"],
            2
        ),
        "%"
    )

    print(
        "Income Change:",
        round(
            result["income_change"],
            2
        ),
        "%"
    )

    print(
        "Expense Change:",
        round(
            result["expense_change"],
            2
        ),
        "%"
    )

    print(
        "Savings Change:",
        round(
            result["savings_change"],
            2
        ),
        "%"
    )

    print(
        "Expense Ratio:",
        round(
            result["expense_ratio"],
            2
        ),
        "%"
    )

    print(
        "\nHighest Spending Category:",
        result["highest_category"]
    )

    print(
        "Highest Spending Amount: ₹",
        round(
            result["highest_amount"],
            2
        )
    )

    print("\n--- Insights ---")

    for insight in result["insights"]:
        print("•", insight)

    print("\n--- Alerts ---")

    if len(result["alerts"]) == 0:

        print("No financial alerts.")

    else:

        for alert in result["alerts"]:
            print("⚠", alert)