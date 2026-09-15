import streamlit as st
from datetime import date
import pandas as pd

from finance import (
    calculate_simple_interest,
    calculate_compound_interest,
    calculate_sip,
    calculate_emi
)

from financial_summary import (
    calculate_financial_summary,
    find_highest_spending_category
)

from spending_analysis import (
    calculate_category_totals,
    calculate_spending_percentages
)

from ai_advisor import (
    create_financial_prompt,
    get_ai_financial_advice
)

from database import (
    save_income,
    save_expense,
    get_all_income,
    get_all_expenses,
    get_monthly_history,
    delete_income,
    delete_expense
)


# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="AI Finance Assistant",
    page_icon="💰",
    layout="wide"
)


# ---------------------------------
# Helper Functions
# ---------------------------------

def load_income():

    rows = get_all_income()

    return [
        {
            "id": row[0],
            "source": row[1],
            "amount": row[2],
            "date": row[3]
        }
        for row in rows
    ]


def load_expenses():

    rows = get_all_expenses()

    return [
        {
            "id": row[0],
            "category": row[1],
            "amount": row[2],
            "date": row[3]
        }
        for row in rows
    ]


def calculate_totals(incomes, expenses):

    total_income = sum(
        income["amount"]
        for income in incomes
    )

    total_expenses = sum(
        expense["amount"]
        for expense in expenses
    )

    remaining_balance = (
        total_income - total_expenses
    )

    if total_income > 0:

        savings_percentage = (
            remaining_balance / total_income
        ) * 100

    else:

        savings_percentage = 0

    return (
        total_income,
        total_expenses,
        remaining_balance,
        savings_percentage
    )


# ---------------------------------
# Load Database Data
# ---------------------------------

incomes = load_income()
expenses = load_expenses()

(
    total_income,
    total_expenses,
    remaining_balance,
    savings_percentage
) = calculate_totals(
    incomes,
    expenses
)


# ---------------------------------
# Sidebar
# ---------------------------------

st.sidebar.title("💰 AI Finance Assistant")

st.sidebar.write(
    "Manage your finances, track spending "
    "and get AI-powered insights."
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Transaction",
        "History",
        "Spending Analysis",
        "Calculators",
        "AI Financial Advisor"
    ]
)


# =================================
# DASHBOARD
# =================================

if page == "Dashboard":

    st.title("💰 AI Finance Assistant")

    st.write(
        "Your personal financial dashboard"
    )

    st.divider()

    # ---------------------------------
    # Financial Metric Cards
    # ---------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Income",
            f"₹{total_income:,.2f}"
        )

    with col2:

        st.metric(
            "Total Expenses",
            f"₹{total_expenses:,.2f}"
        )

    with col3:

        st.metric(
            "Balance",
            f"₹{remaining_balance:,.2f}"
        )

    with col4:

        st.metric(
            "Savings Rate",
            f"{savings_percentage:.2f}%"
        )

    st.divider()

    # ---------------------------------
    # Financial Overview
    # ---------------------------------

    st.subheader("📊 Financial Overview")

    chart_data = pd.DataFrame(
        {
            "Category": [
                "Income",
                "Expenses"
            ],
            "Amount": [
                total_income,
                total_expenses
            ]
        }
    )

    if total_income > 0 or total_expenses > 0:

        st.bar_chart(
            chart_data.set_index("Category")
        )

    else:

        st.info(
            "Add some transactions to see "
            "your financial overview."
        )

    st.divider()

    # ---------------------------------
    # Quick Summary
    # ---------------------------------

    st.subheader("💡 Quick Summary")

    if total_income == 0 and total_expenses == 0:

        st.info(
            "No financial data yet. "
            "Add your first transaction."
        )

    elif remaining_balance < 0:

        st.error(
            "⚠️ Your expenses are currently "
            "higher than your income."
        )

    elif savings_percentage < 20:

        st.warning(
            "Your savings rate is below 20%. "
            "Consider reviewing your expenses."
        )

    elif savings_percentage < 40:

        st.info(
            "Your savings rate is moderate. "
            "Keep working toward higher savings."
        )

    else:

        st.success(
            "🎉 Your savings rate is looking good!"
        )


# =================================
# ADD TRANSACTION
# =================================

elif page == "Add Transaction":

    st.title("➕ Add Transaction")

    st.write(
        "Record your income or expense."
    )

    st.divider()

    # ---------------------------------
    # Transaction Form
    # ---------------------------------

    transaction_type = st.radio(
        "Transaction Type",
        [
            "Income",
            "Expense"
        ],
        horizontal=True
    )

    st.divider()

    # ---------------------------------
    # Income Form
    # ---------------------------------

    if transaction_type == "Income":

        st.subheader("💰 Income Details")

        source = st.selectbox(
            "Income Source",
            [
                "Salary",
                "Freelance",
                "Business",
                "Investment",
                "Other"
            ]
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

        transaction_date = st.date_input(
            "Date",
            value=date.today()
        )

        description = st.text_input(
            "Description (optional)",
            placeholder="Example: September salary"
        )

        if st.button(
            "💾 Save Income",
            type="primary"
        ):

            if amount <= 0:

                st.error(
                    "Please enter an amount greater than 0."
                )

            else:

                save_income(
                    source,
                    amount,
                    transaction_date.strftime(
                        "%Y-%m-%d"
                    )
                )

                st.success(
                    "Income saved successfully! 🎉"
                )

                st.rerun()

    # ---------------------------------
    # Expense Form
    # ---------------------------------

    else:

        st.subheader("💸 Expense Details")

        category = st.selectbox(
            "Expense Category",
            [
                "Food",
                "Rent",
                "Travel",
                "Shopping",
                "Bills",
                "Entertainment",
                "Healthcare",
                "Education",
                "Other"
            ]
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

        transaction_date = st.date_input(
            "Date",
            value=date.today()
        )

        description = st.text_input(
            "Description (optional)",
            placeholder="Example: Lunch with friends"
        )

        if st.button(
            "💾 Save Expense",
            type="primary"
        ):

            if amount <= 0:

                st.error(
                    "Please enter an amount greater than 0."
                )

            else:

                save_expense(
                    category,
                    amount,
                    transaction_date.strftime(
                        "%Y-%m-%d"
                    )
                )

                st.success(
                    "Expense saved successfully! 🎉"
                )

                st.rerun()


# =================================
# HISTORY
# =================================

elif page == "History":

    st.title("📅 Financial History")

    st.write(
        "View your monthly financial performance "
        "and individual transactions."
    )

    st.divider()

    # ---------------------------------
    # Monthly History
    # ---------------------------------

    st.subheader("📊 Monthly Summary")

    history = get_monthly_history()

    if len(history) == 0:

        st.info(
            "No financial history available yet."
        )

    else:

        history_data = []

        for item in history:

            history_data.append(
                {
                    "Month": item["month"],
                    "Income": item["income"],
                    "Expenses": item["expenses"],
                    "Balance": item["balance"],
                    "Savings Rate": (
                        f'{item["savings_rate"]:.2f}%'
                    )
                }
            )

        history_df = pd.DataFrame(
            history_data
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader(
            "📈 Monthly Income vs Expenses"
        )

        chart_df = pd.DataFrame(
            {
                "Income": [
                    item["income"]
                    for item in history
                ],
                "Expenses": [
                    item["expenses"]
                    for item in history
                ]
            },
            index=[
                item["month"]
                for item in history
            ]
        )

        st.bar_chart(chart_df)

    st.divider()

    # ---------------------------------
    # Transaction History
    # ---------------------------------

    st.subheader("🧾 Transaction History")

    income_rows = get_all_income()
    expense_rows = get_all_expenses()

    transactions = []

    for row in income_rows:

        transactions.append(
            {
                "ID": row[0],
                "Date": row[3],
                "Type": "Income",
                "Category / Source": row[1],
                "Amount": row[2]
            }
        )

    for row in expense_rows:

        transactions.append(
            {
                "ID": row[0],
                "Date": row[3],
                "Type": "Expense",
                "Category / Source": row[1],
                "Amount": row[2]
            }
        )

    transactions.sort(
        key=lambda item: item["Date"],
        reverse=True
    )

    if len(transactions) == 0:

        st.info(
            "No transactions recorded yet."
        )

    else:

        transaction_df = pd.DataFrame(
            transactions
        )

        st.dataframe(
            transaction_df,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # ---------------------------------
    # Delete Transactions
    # ---------------------------------

    st.subheader("🗑️ Delete Transaction")

    delete_type = st.selectbox(
        "Select transaction type",
        [
            "Income",
            "Expense"
        ]
    )

    if delete_type == "Income":

        delete_options = income_rows

    else:

        delete_options = expense_rows

    if len(delete_options) == 0:

        st.info(
            "No transactions available to delete."
        )

    else:

        delete_labels = {}

        for row in delete_options:

            delete_labels[
                f"{row[3]} | {row[1]} | ₹{row[2]:,.2f}"
            ] = row[0]

        selected_transaction = st.selectbox(
            "Select transaction",
            list(delete_labels.keys())
        )

        if st.button(
            "Delete Selected Transaction"
        ):

            transaction_id = delete_labels[
                selected_transaction
            ]

            if delete_type == "Income":

                delete_income(
                    transaction_id
                )

            else:

                delete_expense(
                    transaction_id
                )

            st.success(
                "Transaction deleted successfully."
            )

            st.rerun()


# =================================
# SPENDING ANALYSIS
# =================================

elif page == "Spending Analysis":

    st.title("📊 Spending Analysis")

    st.write(
        "Understand where your money is going."
    )

    st.divider()

    if len(expenses) == 0:

        st.info(
            "Add some expenses to see your "
            "spending analysis."
        )

    else:

        category_totals = (
            calculate_category_totals(
                expenses
            )
        )

        category_percentages = (
            calculate_spending_percentages(
                category_totals,
                total_expenses
            )
        )

        # ---------------------------------
        # Spending Metrics
        # ---------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Total Spending",
                f"₹{total_expenses:,.2f}"
            )

        with col2:

            highest_category = max(
                category_totals,
                key=category_totals.get
            )

            highest_amount = (
                category_totals[
                    highest_category
                ]
            )

            st.metric(
                "Highest Spending",
                highest_category,
                f"₹{highest_amount:,.2f}"
            )

        st.divider()

        # ---------------------------------
        # Category Chart
        # ---------------------------------

        st.subheader(
            "💸 Spending By Category"
        )

        spending_df = pd.DataFrame(
            {
                "Category": list(
                    category_totals.keys()
                ),
                "Amount": list(
                    category_totals.values()
                )
            }
        )

        st.bar_chart(
            spending_df.set_index(
                "Category"
            )
        )

        st.divider()

        # ---------------------------------
        # Spending Breakdown
        # ---------------------------------

        st.subheader(
            "📋 Spending Breakdown"
        )

        for category, amount in (
            category_totals.items()
        ):

            percentage = (
                category_percentages[
                    category
                ]
            )

            st.write(
                f"**{category}** — "
                f"₹{amount:,.2f} "
                f"({percentage:.2f}%)"
            )

            st.progress(
                min(
                    percentage / 100,
                    1.0
                )
            )


# =================================
# CALCULATORS
# =================================

elif page == "Calculators":

    st.title("🧮 Financial Calculators")

    calculator = st.selectbox(
        "Choose a calculator",
        [
            "Simple Interest",
            "Compound Interest",
            "SIP Calculator",
            "EMI Calculator"
        ]
    )

    st.divider()

    # ---------------------------------
    # Simple Interest
    # ---------------------------------

    if calculator == "Simple Interest":

        st.subheader(
            "Simple Interest Calculator"
        )

        principal = st.number_input(
            "Principal Amount",
            min_value=0.0,
            step=1000.0
        )

        rate = st.number_input(
            "Annual Interest Rate (%)",
            min_value=0.0,
            step=0.5
        )

        years = st.number_input(
            "Time (Years)",
            min_value=0.1,
            step=1.0
        )

        if st.button(
            "Calculate Simple Interest"
        ):

            interest, amount = (
                calculate_simple_interest(
                    principal,
                    rate,
                    years
                )
            )

            st.success(
                f"Interest: ₹{interest:,.2f}"
            )

            st.info(
                f"Total Amount: ₹{amount:,.2f}"
            )

    # ---------------------------------
    # Compound Interest
    # ---------------------------------

    elif calculator == "Compound Interest":

        st.subheader(
            "Compound Interest Calculator"
        )

        principal = st.number_input(
            "Principal Amount",
            min_value=0.0,
            step=1000.0
        )

        rate = st.number_input(
            "Annual Interest Rate (%)",
            min_value=0.0,
            step=0.5
        )

        years = st.number_input(
            "Time (Years)",
            min_value=0.1,
            step=1.0
        )

        compounds = st.number_input(
            "Compounds Per Year",
            min_value=1,
            step=1
        )

        if st.button(
            "Calculate Compound Interest"
        ):

            interest, amount = (
                calculate_compound_interest(
                    principal,
                    rate,
                    years,
                    compounds
                )
            )

            st.success(
                f"Interest: ₹{interest:,.2f}"
            )

            st.info(
                f"Total Amount: ₹{amount:,.2f}"
            )

    # ---------------------------------
    # SIP
    # ---------------------------------

    elif calculator == "SIP Calculator":

        st.subheader(
            "SIP Calculator"
        )

        monthly_investment = st.number_input(
            "Monthly Investment",
            min_value=0.0,
            step=500.0
        )

        annual_rate = st.number_input(
            "Expected Annual Return (%)",
            min_value=0.0,
            step=0.5
        )

        years = st.number_input(
            "Investment Period (Years)",
            min_value=0.1,
            step=1.0
        )

        if st.button(
            "Calculate SIP"
        ):

            (
                total_invested,
                estimated_returns,
                final_value
            ) = calculate_sip(
                monthly_investment,
                annual_rate,
                years
            )

            st.success(
                f"Total Invested: "
                f"₹{total_invested:,.2f}"
            )

            st.info(
                f"Estimated Returns: "
                f"₹{estimated_returns:,.2f}"
            )

            st.metric(
                "Estimated Final Value",
                f"₹{final_value:,.2f}"
            )

    # ---------------------------------
    # EMI
    # ---------------------------------

    elif calculator == "EMI Calculator":

        st.subheader(
            "EMI Calculator"
        )

        principal = st.number_input(
            "Loan Amount",
            min_value=0.0,
            step=5000.0
        )

        annual_rate = st.number_input(
            "Annual Interest Rate (%)",
            min_value=0.0,
            step=0.5
        )

        years = st.number_input(
            "Loan Period (Years)",
            min_value=0.1,
            step=1.0
        )

        if st.button(
            "Calculate EMI"
        ):

            (
                emi,
                total_interest,
                total_payment
            ) = calculate_emi(
                principal,
                annual_rate,
                years
            )

            st.metric(
                "Monthly EMI",
                f"₹{emi:,.2f}"
            )

            st.info(
                f"Total Interest: "
                f"₹{total_interest:,.2f}"
            )

            st.info(
                f"Total Payment: "
                f"₹{total_payment:,.2f}"
            )


# =================================
# AI FINANCIAL ADVISOR
# =================================

elif page == "AI Financial Advisor":

    st.title("🤖 AI Financial Advisor")

    st.write(
        "Get AI-powered financial guidance "
        "based on your income and spending."
    )

    st.divider()

    # ---------------------------------
    # Financial Information
    # ---------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Total Income:** "
            f"₹{total_income:,.2f}"
        )

        st.write(
            f"**Total Expenses:** "
            f"₹{total_expenses:,.2f}"
        )

        st.write(
            f"**Remaining Balance:** "
            f"₹{remaining_balance:,.2f}"
        )

    with col2:

        st.write(
            f"**Savings Rate:** "
            f"{savings_percentage:.2f}%"
        )

        (
            highest_category,
            highest_amount
        ) = find_highest_spending_category(
            expenses
        )

        if highest_category is not None:

            st.write(
                f"**Highest Spending:** "
                f"{highest_category} "
                f"(₹{highest_amount:,.2f})"
            )

        else:

            st.write(
                "**Highest Spending:** "
                "No expenses recorded"
            )

    st.divider()

    # ---------------------------------
    # Generate AI Advice
    # ---------------------------------

    if st.button(
        "🤖 Generate AI Financial Advice",
        type="primary"
    ):

        if total_income == 0 and total_expenses == 0:

            st.warning(
                "Please add income and expenses "
                "before generating AI advice."
            )

        else:

            prompt = create_financial_prompt(
                total_income,
                total_expenses,
                remaining_balance,
                savings_percentage,
                highest_category,
                highest_amount
            )

            with st.spinner(
                "Gemini is analyzing your financial data..."
            ):

                try:

                    advice = get_ai_financial_advice(
                        prompt
                    )

                    st.success(
                        "AI financial analysis completed!"
                    )

                    st.subheader(
                        "💡 AI Financial Advice"
                    )

                    st.write(advice)

                except Exception as error:

                    st.error(
                        "Unable to generate AI advice."
                    )

                    st.write(
                        "Gemini is currently unavailable. "
                        "Please try again later."
                    )

                    st.caption(
                        f"Technical error: {error}"
                    )