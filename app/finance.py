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