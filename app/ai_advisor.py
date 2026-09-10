from google import genai


# ---------------------------------
# Create Gemini Client
# ---------------------------------

client = genai.Client()


# ---------------------------------
# Create Financial Prompt
# ---------------------------------

def create_financial_prompt(
    total_income,
    total_expenses,
    remaining_balance,
    savings_percentage,
    highest_category,
    highest_amount
):

    if highest_category is None:

        highest_category = "No expenses recorded"
        highest_amount = 0

    prompt = f"""
You are a helpful personal finance assistant.

Analyze the following financial information:

Total Income: ₹{total_income:.2f}
Total Expenses: ₹{total_expenses:.2f}
Remaining Balance: ₹{remaining_balance:.2f}
Savings Percentage: {savings_percentage:.2f}%
Highest Spending Category: {highest_category}
Highest Spending Amount: ₹{highest_amount:.2f}

Provide simple and practical financial guidance.

Your response should include:

1. A short analysis of the user's financial situation.
2. The main spending concern.
3. Two or three practical suggestions.
4. One positive financial habit the user should continue.

Do not provide investment recommendations or guarantees.

Use simple language that a beginner can understand.
"""

    return prompt


# ---------------------------------
# Get AI Financial Advice
# ---------------------------------

def get_ai_financial_advice(prompt):

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt
    )

    return response.text


# ---------------------------------
# Show AI Financial Advice
# ---------------------------------

def show_ai_prompt(
    total_income,
    total_expenses,
    remaining_balance,
    savings_percentage,
    highest_category,
    highest_amount
):

    prompt = create_financial_prompt(
        total_income,
        total_expenses,
        remaining_balance,
        savings_percentage,
        highest_category,
        highest_amount
    )

    print("\n=================================")
    print("       AI Financial Advisor")
    print("=================================")

    print(
        "\nAnalyzing your financial information..."
    )

    try:

        advice = get_ai_financial_advice(prompt)

        print("\n--- AI Financial Advice ---")
        print(advice)

    except Exception as error:

        print("\nUnable to get AI advice.")
        print("Error:", error)


# ---------------------------------
# Test
# ---------------------------------

if __name__ == "__main__":

    total_income = 60000
    total_expenses = 27000
    remaining_balance = 33000
    savings_percentage = 55
    highest_category = "Rent"
    highest_amount = 15000

    show_ai_prompt(
        total_income,
        total_expenses,
        remaining_balance,
        savings_percentage,
        highest_category,
        highest_amount
    )


