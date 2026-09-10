def calculate_simple_interest(principal, rate, time):
    interest = (principal * rate * time) / 100
    amount = principal + interest

    return interest, amount


def calculate_compound_interest(principal, rate, time, compounds_per_year):
    amount = principal * (
        1 + rate / (100 * compounds_per_year)
    ) ** (compounds_per_year * time)

    interest = amount - principal

    return interest, amount


def calculate_sip(monthly_investment, annual_rate, years):
    months = years * 12
    monthly_rate = annual_rate / (12 * 100)

    future_value = monthly_investment * (
        ((1 + monthly_rate) ** months - 1)
        / monthly_rate
    ) * (1 + monthly_rate)

    total_invested = monthly_investment * months
    estimated_returns = future_value - total_invested

    return total_invested, estimated_returns, future_value

def calculate_emi(principal, annual_rate, years):
    monthly_rate = annual_rate / (12 * 100)
    months = years * 12

    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = (
            principal
            * monthly_rate
            * (1 + monthly_rate) ** months
        ) / (
            (1 + monthly_rate) ** months - 1
        )

    total_payment = emi * months
    total_interest = total_payment - principal

    return emi, total_interest, total_payment