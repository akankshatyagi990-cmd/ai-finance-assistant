from finance import calculate_simple_interest, calculate_compound_interest

print("Welcome to AI Finance Assistant!")

print("\nChoose a calculation:")
print("1. Simple Interest")
print("2. Compound Interest")

choice = input("Enter your choice (1 or 2): ")

try:
    principal = float(input("Enter principal amount: "))
    rate = float(input("Enter annual interest rate (%): "))
    time = float(input("Enter time in years: "))

    if principal <= 0 or rate < 0 or time <= 0:
        print("Please enter valid positive values.")

    elif choice == "1":
        interest, amount = calculate_simple_interest(
            principal, rate, time
        )

        print("\n--- Simple Interest Result ---")
        print("Principal:", principal)
        print("Interest:", interest)
        print("Total Amount:", amount)

    elif choice == "2":
        compounds_per_year = int(
            input("Enter number of times compounded per year: ")
        )

        if compounds_per_year <= 0:
            print("Compounding frequency must be greater than 0.")
        else:
            interest, amount = calculate_compound_interest(
                principal,
                rate,
                time,
                compounds_per_year
            )

            print("\n--- Compound Interest Result ---")
            print("Principal:", principal)
            print("Interest:", round(interest, 2))
            print("Total Amount:", round(amount, 2))

    else:
        print("Invalid choice. Please select 1 or 2.")

except ValueError:
    print("Invalid input. Please enter numbers only.")