from database import save_income


def add_income(incomes, source, amount, date):

    income = {
        "source": source,
        "amount": amount,
        "date": date
    }

    incomes.append(income)

    save_income(
        source,
        amount,
        date
    )


def calculate_total_income(incomes):

    total = 0

    for income in incomes:
        total = total + income["amount"]

    return total


def show_income(incomes):

    print("\n--- Income List ---")

    if len(incomes) == 0:

        print("No income recorded.")
        return

    for income in incomes:

        print(
            income["date"],
            "|",
            income["source"],
            "| ₹",
            round(income["amount"], 2)
        )


def show_income_summary(incomes):

    source_totals = {}

    for income in incomes:

        source = income["source"]
        amount = income["amount"]

        if source in source_totals:

            source_totals[source] = (
                source_totals[source] + amount
            )

        else:

            source_totals[source] = amount

    print("\n--- Income Summary ---")

    if len(source_totals) == 0:

        print("No income recorded.")
        return

    for source, amount in source_totals.items():

        print(
            source,
            "₹",
            round(amount, 2)
        )


def run_income_tracker(incomes):

    print("\n=================================")
    print("        Income Tracker")
    print("=================================")

    while True:

        print("\nChoose an option:")
        print("1. Add Income")
        print("2. View Income")
        print("3. View Income Summary")
        print("4. View Total Income")
        print("5. Return to Main Menu")

        choice = input(
            "\nEnter your choice: "
        )

        if choice == "1":

            source = input(
                "Enter income source: "
            )

            date = input(
                "Enter date (YYYY-MM-DD): "
            )

            try:

                amount = float(
                    input(
                        "Enter income amount: "
                    )
                )

                if amount <= 0:

                    print(
                        "Amount must be greater than 0."
                    )

                else:

                    add_income(
                        incomes,
                        source,
                        amount,
                        date
                    )

                    print(
                        "Income added successfully."
                    )

            except ValueError:

                print(
                    "Invalid amount. "
                    "Please enter a number."
                )

        elif choice == "2":

            show_income(incomes)

        elif choice == "3":

            show_income_summary(incomes)

        elif choice == "4":

            total = calculate_total_income(
                incomes
            )

            print(
                "\nTotal Income: ₹",
                round(total, 2)
            )

        elif choice == "5":

            print(
                "\nReturning to Main Menu..."
            )

            break

        else:

            print(
                "Invalid choice. "
                "Please select 1 to 5."
            )


if __name__ == "__main__":

    incomes = []

    run_income_tracker(incomes)

