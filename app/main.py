from finance import calculate_simple_interest

print("Welcome to AI Finance Assistant!")

try:
    principal = float(input("Enter principal amount: "))
    rate = float(input("Enter annual interest rate (%): "))
    time = float(input("Enter time in years: "))

    if principal <= 0 or rate < 0 or time <= 0:
        print("Please enter valid positive values.")
    else:
        interest, amount = calculate_simple_interest(
            principal, rate, time
        )

        print("\n--- Finance Result ---")
        print("Principal:", principal)
        print("Interest:", interest)
        print("Total Amount:", amount)

except ValueError:
    print("Invalid input. Please enter numbers only.")