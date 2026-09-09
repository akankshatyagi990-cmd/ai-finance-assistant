from finance import calculate_simple_interest

print("Welcome to AI Finance Assistant!")

principal = 50000
rate = 8
time = 2

interest, amount = calculate_simple_interest(principal, rate, time)

print("\n--- Finance Result ---")
print("Principal:", principal)
print("Interest:", interest)
print("Total Amount:", amount)