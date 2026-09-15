def calculate_financial_health_score(
    total_income,
    total_expenses,
    savings_percentage
):
    """
    Calculate a simple financial health score from 0 to 100.

    The score is based mainly on:
    - Savings percentage
    - Expense-to-income ratio
    - Whether the user has positive remaining balance
    """

    if total_income <= 0:
        return 0, "No Income Data"

    score = 0

    # --------------------------------
    # 1. Savings Score
    # --------------------------------
    if savings_percentage >= 30:
        score += 40
    elif savings_percentage >= 20:
        score += 35
    elif savings_percentage >= 10:
        score += 25
    elif savings_percentage > 0:
        score += 15
    else:
        score += 0

    # --------------------------------
    # 2. Expense Ratio Score
    # --------------------------------
    expense_ratio = (total_expenses / total_income) * 100

    if expense_ratio <= 50:
        score += 30
    elif expense_ratio <= 70:
        score += 25
    elif expense_ratio <= 85:
        score += 15
    elif expense_ratio <= 100:
        score += 5
    else:
        score += 0

    # --------------------------------
    # 3. Positive Balance Score
    # --------------------------------
    remaining_balance = total_income - total_expenses

    if remaining_balance > 0:
        score += 30
    elif remaining_balance == 0:
        score += 10
    else:
        score += 0

    # --------------------------------
    # Determine Health Level
    # --------------------------------
    if score >= 80:
        health_level = "Excellent"
    elif score >= 60:
        health_level = "Good"
    elif score >= 40:
        health_level = "Fair"
    elif score >= 20:
        health_level = "Needs Attention"
    else:
        health_level = "Critical"

    return score, health_level