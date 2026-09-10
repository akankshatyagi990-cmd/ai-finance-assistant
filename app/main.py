from finance import (
    calculate_simple_interest,
    calculate_compound_interest,
    calculate_sip
)


print("=================================")
print("     AI Finance Assistant")
print("=================================")

print("\nChoose a calculation:")
print("1. Simple Interest")
print("2. Compound Interest")
print("3. SIP Calculator")

choice = input("\nEnter your choice (1, 2 or 3): ")


try:

    # -------------------------------
    # Simple Interest
    # -------------------------------
    if choice == "1":

        principal = float(input("Enter principal amount: "))
        rate = float(input("Enter annual interest rate (%): "))
        time = float(input("Enter time in years: "))

        if principal <= 0 or rate < 0 or time <= 0:
            print("\nPlease enter valid values.")

        else:
            interest, amount = calculate_simple_interest(
                principal,
                rate,
                time
            )

            print("\n--- Simple Interest Result ---")
            print("Principal:", round(principal, 2))
            print("Interest:", round(interest, 2))
            print("Total Amount:", round(amount, 2))


    # -------------------------------
    # Compound Interest
    # -------------------------------
    elif choice == "2":

        principal = float(input("Enter principal amount: "))
        rate = float(input("Enter annual interest rate (%): "))
        time = float(input("Enter time in years: "))
        compounds_per_year = int(
            input("Enter number of times compounded per year: ")
        )

        if principal <= 0 or rate < 0 or time <= 0:
            print("\nPlease enter valid values.")

        elif compounds_per_year <= 0:
            print("\nCompounding frequency must be greater than 0.")

        else:
            interest, amount = calculate_compound_interest(
                principal,
                rate,
                time,
                compounds_per_year
            )

            print("\n--- Compound Interest Result ---")
            print("Principal:", round(principal, 2))
            print("Interest:", round(interest, 2))
            print("Total Amount:", round(amount, 2))


    # -------------------------------
    # SIP
    # -------------------------------
    elif choice == "3":

        monthly_investment = float(
            input("Enter monthly investment amount: ")
        )
        annual_rate = float(
            input("Enter expected annual return rate (%): ")
        )
        years = float(
            input("Enter investment period in years: ")
        )

        if monthly_investment <= 0 or annual_rate < 0 or years <= 0:
            print("\nPlease enter valid values.")

        else:
            total_invested, estimated_returns, final_value = calculate_sip(
                monthly_investment,
                annual_rate,
                years
            )

            print("\n--- SIP Result ---")
            print("Monthly Investment:", round(monthly_investment, 2))
            print("Total Invested:", round(total_invested, 2))
            print("Estimated Returns:", round(estimated_returns, 2))
            print("Final Value:", round(final_value, 2))


    # -------------------------------
    # Invalid Choice
    # -------------------------------
    else:
        print("\nInvalid choice. Please select 1, 2 or 3.")


except ValueError:
    print("\nInvalid input. Please enter numbers only.")