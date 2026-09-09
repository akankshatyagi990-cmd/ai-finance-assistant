from finance import calculate_simple_interest

print("Welcome to AI Finance Assistant!")

principal = float(input("Enter principal amount: "))
rate = float(input("Enter annual interest rate (%): "))
time = float(input("Enter time in years: "))

interest, amount = calculate_simple_interest(principal, rate, time)

print("\n--- Finance Result ---")
print("Principal:", principal)
print("Interest:", interest)
print("Total Amount:", amount)