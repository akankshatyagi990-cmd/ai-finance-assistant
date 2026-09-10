def generate_financial_advice(
    savings_percentage,
    highest_category,
    highest_amount,
    remaining_balance
):

    print("\n=================================")
    print("       AI Financial Advisor")
    print("=================================")

    print(
        "\nYour savings rate:",
        round(savings_percentage, 2),
        "%"
    )

    if highest_category is not None:

        print(
            "Highest spending category:",
            highest_category
        )

        print(
            "Highest spending amount: ₹",
            round(highest_amount, 2)
        )

    print(
        "Remaining balance: ₹",
        round(remaining_balance, 2)
    )

    print("\n--- Financial Advice ---")

    if remaining_balance < 0:

        print(
            "Your expenses are higher than your income."
        )

        print(
            "Try to reduce unnecessary expenses "
            "and review your highest spending category."
        )

    elif savings_percentage < 20:

        print(
            "Your savings rate is below 20%."
        )

        print(
            "Consider reducing unnecessary expenses "
            "and increasing your monthly savings."
        )

    elif savings_percentage < 40:

        print(
            "Your savings rate is moderate."
        )

        print(
            "Try to increase your savings gradually "
            "by controlling your major expenses."
        )

    else:

        print(
            "Your savings rate is good."
        )

        print(
            "Keep tracking your expenses and "
            "maintain your current savings habit."
        )

    if highest_category is not None:

        print(
            "\nFocus Area:",
            highest_category
        )

        print(
            "This is currently your highest spending "
            "category. Review this expense to see "
            "if you can reduce it."
        )


def run_financial_advisor(
    savings_percentage,
    highest_category,
    highest_amount,
    remaining_balance
):

    generate_financial_advice(
        savings_percentage,
        highest_category,
        highest_amount,
        remaining_balance
    )


if __name__ == "__main__":

    # Sample data for testing
    savings_percentage = 40
    highest_category = "Rent"
    highest_amount = 15000
    remaining_balance = 24000

    run_financial_advisor(
        savings_percentage,
        highest_category,
        highest_amount,
        remaining_balance
    )