def calculate_budget_status(category_budgets, category_totals):
    """
    Compare the user's budget with actual spending.

    category_budgets:
        Dictionary containing budget amounts for each category.

    category_totals:
        Dictionary containing actual spending for each category.
    """

    budget_status = {}

    for category, budget in category_budgets.items():

        spent = category_totals.get(category, 0)

        remaining = budget - spent

        if budget > 0:
            percentage_used = (spent / budget) * 100
        else:
            percentage_used = 0

        if spent > budget:
            status = "Over Budget"
        elif percentage_used >= 80:
            status = "Almost Reached"
        else:
            status = "Within Budget"

        budget_status[category] = {
            "budget": budget,
            "spent": spent,
            "remaining": remaining,
            "percentage_used": percentage_used,
            "status": status
        }

    return budget_status


def calculate_total_budget(category_budgets):
    """
    Calculate the total budget across all categories.
    """

    return sum(category_budgets.values())


def calculate_total_spending(category_totals):
    """
    Calculate total spending across all categories.
    """

    return sum(category_totals.values())


def calculate_remaining_budget(total_budget, total_spending):
    """
    Calculate how much budget is remaining.
    """

    return total_budget - total_spending