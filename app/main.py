from finance import (
    calculate_simple_interest,
    calculate_compound_interest,
    calculate_sip,
    calculate_emi
)

from expense_tracker import (
    run_expense_tracker,
    calculate_total_expenses
)

from income_tracker import (
    run_income_tracker,
    calculate_total_income
)

from financial_summary import (
    calculate_financial_summary,
    find_highest_spending_category,
    show_financial_summary
)

from financial_advisor import run_financial_advisor

from spending_analysis import show_spending_analysis


# Shared data
expenses = []
incomes = []


print("=================================")
print("     AI Finance Assistant")
print("=================================")


while True:

    print("\nChoose an option:")
    print("1. Simple Interest")
    print("2. Compound Interest")
    print("3. SIP Calculator")
    print("4. EMI Calculator")
    print("5. Expense Tracker")
    print("6. Income Tracker")
    print("7. Financial Summary")
    print("8. Financial Advisor")
    print("9. Spending Analysis")
    print("10. Exit")

    choice = input("\nEnter your choice (1-10): ")

    try:

        # -------------------------------
        # Simple Interest
        # -------------------------------
        if choice == "1":

            principal = float(
                input("Enter principal amount: ")
            )

            rate = float(
                input("Enter annual interest rate (%): ")
            )

            time = float(
                input("Enter time in years: ")
            )

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

            principal = float(
                input("Enter principal amount: ")
            )

            rate = float(
                input("Enter annual interest rate (%): ")
            )

            time = float(
                input("Enter time in years: ")
            )

            compounds_per_year = int(
                input(
                    "Enter number of times compounded per year: "
                )
            )

            if principal <= 0 or rate < 0 or time <= 0:

                print("\nPlease enter valid values.")

            elif compounds_per_year <= 0:

                print(
                    "\nCompounding frequency "
                    "must be greater than 0."
                )

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
        # SIP Calculator
        # -------------------------------
        elif choice == "3":

            monthly_investment = float(
                input("Enter monthly investment amount: ")
            )

            annual_rate = float(
                input(
                    "Enter expected annual return rate (%): "
                )
            )

            years = float(
                input("Enter investment period in years: ")
            )

            if (
                monthly_investment <= 0
                or annual_rate < 0
                or years <= 0
            ):

                print("\nPlease enter valid values.")

            else:

                (
                    total_invested,
                    estimated_returns,
                    final_value
                ) = calculate_sip(
                    monthly_investment,
                    annual_rate,
                    years
                )

                print("\n--- SIP Result ---")

                print(
                    "Monthly Investment:",
                    round(monthly_investment, 2)
                )

                print(
                    "Total Invested:",
                    round(total_invested, 2)
                )

                print(
                    "Estimated Returns:",
                    round(estimated_returns, 2)
                )

                print(
                    "Final Value:",
                    round(final_value, 2)
                )


        # -------------------------------
        # EMI Calculator
        # -------------------------------
        elif choice == "4":

            principal = float(
                input("Enter loan amount: ")
            )

            annual_rate = float(
                input("Enter annual interest rate (%): ")
            )

            years = float(
                input("Enter loan period in years: ")
            )

            if (
                principal <= 0
                or annual_rate < 0
                or years <= 0
            ):

                print("\nPlease enter valid values.")

            else:

                (
                    emi,
                    total_interest,
                    total_payment
                ) = calculate_emi(
                    principal,
                    annual_rate,
                    years
                )

                print("\n--- EMI Result ---")

                print(
                    "Loan Amount:",
                    round(principal, 2)
                )

                print(
                    "Monthly EMI:",
                    round(emi, 2)
                )

                print(
                    "Total Interest:",
                    round(total_interest, 2)
                )

                print(
                    "Total Payment:",
                    round(total_payment, 2)
                )


        # -------------------------------
        # Expense Tracker
        # -------------------------------
        elif choice == "5":

            run_expense_tracker(expenses)


        # -------------------------------
        # Income Tracker
        # -------------------------------
        elif choice == "6":

            run_income_tracker(incomes)


        # -------------------------------
        # Financial Summary
        # -------------------------------
        elif choice == "7":

            total_income = calculate_total_income(
                incomes
            )

            total_expenses = calculate_total_expenses(
                expenses
            )

            show_financial_summary(
                total_income,
                total_expenses,
                expenses
            )


        # -------------------------------
        # Financial Advisor
        # -------------------------------
        elif choice == "8":

            total_income = calculate_total_income(
                incomes
            )

            total_expenses = calculate_total_expenses(
                expenses
            )

            (
                remaining_balance,
                savings_percentage
            ) = calculate_financial_summary(
                total_income,
                total_expenses
            )

            (
                highest_category,
                highest_amount
            ) = find_highest_spending_category(
                expenses
            )

            run_financial_advisor(
                savings_percentage,
                highest_category,
                highest_amount,
                remaining_balance
            )


        # -------------------------------
        # Spending Analysis
        # -------------------------------
        elif choice == "9":

            show_spending_analysis(
                expenses
            )


        # -------------------------------
        # Exit
        # -------------------------------
        elif choice == "10":

            print(
                "\nThank you for using "
                "AI Finance Assistant!"
            )

            break


        # -------------------------------
        # Invalid Choice
        # -------------------------------
        else:

            print(
                "\nInvalid choice. "
                "Please select 1 to 10."
            )


    except ValueError:

        print(
            "\nInvalid input. "
            "Please enter numbers only."
        )