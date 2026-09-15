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


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Finance Assistant",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PROFESSIONAL STYLING
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- Main Application ---------- */

    .stApp {
        background-color: #0b0f14;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }


    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        background-color: #11161d;
        border-right: 1px solid #242b35;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
        padding-left: 1.3rem;
        padding-right: 1.3rem;
    }

    .sidebar-brand {
        font-size: 1.15rem;
        font-weight: 700;
        color: #f4f7fa;
        letter-spacing: -0.3px;
        margin-bottom: 0.3rem;
    }

    .sidebar-subtitle {
        font-size: 0.78rem;
        color: #8d98a7;
        line-height: 1.5;
        margin-bottom: 2rem;
    }


    /* ---------- Typography ---------- */

    h1 {
        font-size: 2.35rem !important;
        font-weight: 700 !important;
        letter-spacing: -1px !important;
        color: #f5f7fa !important;
    }

    h2 {
        font-size: 1.45rem !important;
        font-weight: 650 !important;
        color: #f0f3f6 !important;
    }

    h3 {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: #e7ebef !important;
    }

    p {
        color: #9ca7b5;
    }


    /* ---------- Page Header ---------- */

    .page-eyebrow {
        color: #7f8b99;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 0.45rem;
    }

    .page-description {
        color: #8f9aa8;
        font-size: 0.92rem;
        margin-top: -0.8rem;
        margin-bottom: 2rem;
    }


    /* ---------- KPI Cards ---------- */

    .metric-card {
        background: #121820;
        border: 1px solid #242d38;
        border-radius: 12px;
        padding: 1.25rem 1.35rem;
        min-height: 125px;
    }

    .metric-label {
        color: #8793a1;
        font-size: 0.76rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        margin-bottom: 0.7rem;
    }

    .metric-value {
        color: #f4f6f8;
        font-size: 1.65rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    .metric-small {
        color: #7f8b98;
        font-size: 0.75rem;
        margin-top: 0.45rem;
    }


    /* ---------- Content Cards ---------- */

    .content-card {
        background: #121820;
        border: 1px solid #242d38;
        border-radius: 12px;
        padding: 1.35rem;
        margin-bottom: 1rem;
    }

    .card-title {
        color: #eef1f4;
        font-size: 1rem;
        font-weight: 650;
        margin-bottom: 0.2rem;
    }

    .card-subtitle {
        color: #7f8b98;
        font-size: 0.78rem;
        margin-bottom: 1rem;
    }


    /* ---------- Financial Health ---------- */

    .health-score {
        font-size: 3rem;
        font-weight: 750;
        color: #f4f6f8;
        line-height: 1;
    }

    .health-label {
        color: #7f8b98;
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }


    /* ---------- Insight Card ---------- */

    .insight-card {
        background: #151c25;
        border: 1px solid #293340;
        border-radius: 12px;
        padding: 1.35rem;
    }

    .insight-label {
        color: #8d99a8;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.55rem;
    }

    .insight-text {
        color: #e9edf1;
        font-size: 0.95rem;
        line-height: 1.55;
    }


    /* ---------- Section Label ---------- */

    .section-label {
        color: #e9edf1;
        font-size: 1.05rem;
        font-weight: 650;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
    }


    /* ---------- Transaction Rows ---------- */

    .transaction-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #121820;
        border: 1px solid #242d38;
        border-radius: 9px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.55rem;
    }

    .transaction-name {
        color: #e7ebef;
        font-weight: 600;
        font-size: 0.88rem;
    }

    .transaction-date {
        color: #727e8d;
        font-size: 0.72rem;
        margin-top: 0.2rem;
    }

    .transaction-income {
        color: #5fd18b;
        font-weight: 650;
    }

    .transaction-expense {
        color: #e47c7c;
        font-weight: 650;
    }


    /* ---------- Buttons ---------- */

    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        min-height: 42px;
    }


    /* ---------- Tables ---------- */

    [data-testid="stDataFrame"] {
        border: 1px solid #242d38;
        border-radius: 10px;
        overflow: hidden;
    }


    /* ---------- Dividers ---------- */

    hr {
        border-color: #242b35 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

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
        item["amount"]
        for item in incomes
    )

    total_expenses = sum(
        item["amount"]
        for item in expenses
    )

    balance = total_income - total_expenses

    if total_income > 0:

        savings_rate = (
            balance / total_income
        ) * 100

    else:

        savings_rate = 0

    return (
        total_income,
        total_expenses,
        balance,
        savings_rate
    )


def calculate_health_score(
    savings_rate,
    total_income,
    total_expenses
):

    if total_income == 0:

        return 0

    score = 0

    # Savings component
    if savings_rate >= 50:
        score += 50

    elif savings_rate >= 30:
        score += 40

    elif savings_rate >= 20:
        score += 30

    elif savings_rate >= 10:
        score += 20

    elif savings_rate > 0:
        score += 10

    # Expense-to-income component
    expense_ratio = (
        total_expenses / total_income
    ) * 100

    if expense_ratio <= 30:
        score += 40

    elif expense_ratio <= 50:
        score += 30

    elif expense_ratio <= 70:
        score += 20

    elif expense_ratio <= 90:
        score += 10

    # Basic activity component
    score += 10

    return min(score, 100)


def get_health_label(score):

    if score >= 80:
        return "Strong financial position"

    elif score >= 60:
        return "Healthy financial position"

    elif score >= 40:
        return "Needs improvement"

    else:
        return "Needs attention"


def format_currency(amount):

    return f"₹{amount:,.0f}"


# =========================================================
# LOAD DATA
# =========================================================

incomes = load_income()
expenses = load_expenses()

(
    total_income,
    total_expenses,
    balance,
    savings_rate
) = calculate_totals(
    incomes,
    expenses
)

health_score = calculate_health_score(
    savings_rate,
    total_income,
    total_expenses
)

health_label = get_health_label(
    health_score
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        AI Finance Assistant
    </div>

    <div class="sidebar-subtitle">
        Personal financial intelligence
        and spending management.
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "**Workspace**"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Transaction",
        "History",
        "Spending Analysis",
        "Calculators",
        "AI Financial Advisor"
    ],
    label_visibility="collapsed"
)

st.sidebar.divider()

st.sidebar.caption(
    "AI Finance Assistant · Portfolio Project"
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.markdown(
        '<div class="page-eyebrow">Financial overview</div>',
        unsafe_allow_html=True
    )

    st.title("Dashboard")

    st.markdown(
        """
        <div class="page-description">
            A clear view of your income, spending and financial position.
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------
    # KPI CARDS
    # -----------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Total Income</div>
                <div class="metric-value">
                    {format_currency(total_income)}
                </div>
                <div class="metric-small">
                    Recorded income
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Total Expenses</div>
                <div class="metric-value">
                    {format_currency(total_expenses)}
                </div>
                <div class="metric-small">
                    Recorded spending
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Available Balance</div>
                <div class="metric-value">
                    {format_currency(balance)}
                </div>
                <div class="metric-small">
                    Income minus expenses
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Savings Rate</div>
                <div class="metric-value">
                    {savings_rate:.1f}%
                </div>
                <div class="metric-small">
                    Based on recorded income
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # -----------------------------------------
    # HEALTH + INSIGHT
    # -----------------------------------------

    col1, col2 = st.columns([1, 2])

    with col1:

        st.markdown(
            """
            <div class="content-card">
                <div class="card-title">
                    Financial Health
                </div>
                <div class="card-subtitle">
                    Based on savings and spending behaviour
                </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
                <div class="health-score">
                    {health_score}
                    <span style="font-size:1.1rem;color:#7f8b98;">
                        / 100
                    </span>
                </div>

                <div class="health-label">
                    {health_label}
                </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(
            health_score / 100
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    with col2:

        if balance < 0:

            insight = (
                "Your current expenses are higher than "
                "your recorded income. Reviewing your "
                "largest spending categories could help "
                "improve your financial position."
            )

        elif savings_rate < 20:

            insight = (
                "Your savings rate is currently below "
                "20%. Consider reviewing recurring and "
                "discretionary expenses."
            )

        elif savings_rate < 40:

            insight = (
                "Your savings rate is moderate. "
                "Maintaining consistent expense tracking "
                "could help you gradually improve it."
            )

        else:

            insight = (
                "Your current savings rate is strong. "
                "Continue monitoring your spending and "
                "maintaining consistent savings habits."
            )

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-label">
                    Financial Insight
                </div>

                <div class="insight-text">
                    {insight}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # -----------------------------------------
    # MONTHLY TREND + SPENDING
    # -----------------------------------------

    left, right = st.columns([1.6, 1])

    with left:

        st.markdown(
            """
            <div class="section-label">
                Monthly Financial Trend
            </div>
            """,
            unsafe_allow_html=True
        )

        history = get_monthly_history()

        if len(history) > 0:

            chart_data = pd.DataFrame(
                {
                    "Income": [
                        item["income"]
                        for item in reversed(history)
                    ],
                    "Expenses": [
                        item["expenses"]
                        for item in reversed(history)
                    ]
                },
                index=[
                    item["month"]
                    for item in reversed(history)
                ]
            )

            st.line_chart(
                chart_data,
                height=330
            )

        else:

            st.info(
                "Add transactions to build your monthly trend."
            )

    with right:

        st.markdown(
            """
            <div class="section-label">
                Spending Breakdown
            </div>
            """,
            unsafe_allow_html=True
        )

        if len(expenses) > 0:

            category_totals = (
                calculate_category_totals(
                    expenses
                )
            )

            spending_df = pd.DataFrame(
                {
                    "Amount": category_totals
                }
            )

            st.bar_chart(
                spending_df,
                height=330
            )

        else:

            st.info(
                "No spending data available yet."
            )

    # -----------------------------------------
    # RECENT TRANSACTIONS
    # -----------------------------------------

    st.markdown(
        """
        <div class="section-label">
            Recent Transactions
        </div>
        """,
        unsafe_allow_html=True
    )

    transactions = []

    for item in incomes:

        transactions.append(
            {
                "date": item["date"],
                "name": item["source"],
                "type": "Income",
                "amount": item["amount"]
            }
        )

    for item in expenses:

        transactions.append(
            {
                "date": item["date"],
                "name": item["category"],
                "type": "Expense",
                "amount": item["amount"]
            }
        )

    transactions.sort(
        key=lambda x: x["date"],
        reverse=True
    )

    if len(transactions) > 0:

        for transaction in transactions[:5]:

            amount_class = (
                "transaction-income"
                if transaction["type"] == "Income"
                else "transaction-expense"
            )

            sign = (
                "+"
                if transaction["type"] == "Income"
                else "-"
            )

            st.markdown(
                f"""
                <div class="transaction-row">

                    <div>
                        <div class="transaction-name">
                            {transaction["name"]}
                        </div>

                        <div class="transaction-date">
                            {transaction["date"]}
                            · {transaction["type"]}
                        </div>
                    </div>

                    <div class="{amount_class}">
                        {sign} ₹{transaction["amount"]:,.2f}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No transactions recorded yet."
        )


# =========================================================
# ADD TRANSACTION
# =========================================================

elif page == "Add Transaction":

    st.markdown(
        '<div class="page-eyebrow">Transactions</div>',
        unsafe_allow_html=True
    )

    st.title("Add Transaction")

    st.markdown(
        """
        <div class="page-description">
            Record an income or expense and keep your financial history up to date.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Center the form
    left_space, form_col, right_space = st.columns(
        [1, 2, 1]
    )

    with form_col:

        st.markdown(
            '<div class="content-card">',
            unsafe_allow_html=True
        )

        transaction_type = st.radio(
            "Transaction type",
            [
                "Income",
                "Expense"
            ],
            horizontal=True
        )

        st.write("")

        if transaction_type == "Income":

            source = st.selectbox(
                "Income source",
                [
                    "Salary",
                    "Freelance",
                    "Business",
                    "Investment",
                    "Other"
                ]
            )

        else:

            source = st.selectbox(
                "Expense category",
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
            "Description",
            placeholder="Optional note about this transaction"
        )

        st.write("")

        if transaction_type == "Income":

            save_button = st.button(
                "Save Income",
                type="primary",
                use_container_width=True
            )

        else:

            save_button = st.button(
                "Save Expense",
                type="primary",
                use_container_width=True
            )

        if save_button:

            if amount <= 0:

                st.error(
                    "Please enter an amount greater than zero."
                )

            else:

                formatted_date = (
                    transaction_date.strftime(
                        "%Y-%m-%d"
                    )
                )

                if transaction_type == "Income":

                    save_income(
                        source,
                        amount,
                        formatted_date
                    )

                    st.success(
                        "Income saved successfully."
                    )

                else:

                    save_expense(
                        source,
                        amount,
                        formatted_date
                    )

                    st.success(
                        "Expense saved successfully."
                    )

                st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    st.caption(
        "Transactions are stored locally in your SQLite database."
    )


# =========================================================
# HISTORY
# =========================================================

elif page == "History":

    st.markdown(
        '<div class="page-eyebrow">Records</div>',
        unsafe_allow_html=True
    )

    st.title("Financial History")

    st.markdown(
        """
        <div class="page-description">
            Review your monthly financial performance and transaction history.
        </div>
        """,
        unsafe_allow_html=True
    )

    history = get_monthly_history()

    # -----------------------------------------
    # Monthly Summary
    # -----------------------------------------

    st.markdown(
        '<div class="section-label">Monthly Summary</div>',
        unsafe_allow_html=True
    )

    if len(history) == 0:

        st.info(
            "No monthly financial history available yet."
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
                        f'{item["savings_rate"]:.1f}%'
                    )
                }
            )

        history_df = pd.DataFrame(
            history_data
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Income": st.column_config.NumberColumn(
                    "Income",
                    format="₹%.2f"
                ),
                "Expenses": st.column_config.NumberColumn(
                    "Expenses",
                    format="₹%.2f"
                ),
                "Balance": st.column_config.NumberColumn(
                    "Balance",
                    format="₹%.2f"
                )
            }
        )

        st.markdown(
            '<div class="section-label">Monthly Income vs Expenses</div>',
            unsafe_allow_html=True
        )

        chart_df = pd.DataFrame(
            {
                "Income": [
                    item["income"]
                    for item in reversed(history)
                ],
                "Expenses": [
                    item["expenses"]
                    for item in reversed(history)
                ]
            },
            index=[
                item["month"]
                for item in reversed(history)
            ]
        )

        st.line_chart(
            chart_df,
            height=350
        )

    st.divider()

    # -----------------------------------------
    # Transaction History
    # -----------------------------------------

    st.markdown(
        '<div class="section-label">Transaction History</div>',
        unsafe_allow_html=True
    )

    income_rows = get_all_income()
    expense_rows = get_all_expenses()

    transactions = []

    for row in income_rows:

        transactions.append(
            {
                "Date": row[3],
                "Type": "Income",
                "Category / Source": row[1],
                "Amount": row[2]
            }
        )

    for row in expense_rows:

        transactions.append(
            {
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
            hide_index=True,
            column_config={
                "Amount": st.column_config.NumberColumn(
                    "Amount",
                    format="₹%.2f"
                )
            }
        )

    st.divider()

    # -----------------------------------------
    # Delete Transaction
    # -----------------------------------------

    st.markdown(
        '<div class="section-label">Manage Transactions</div>',
        unsafe_allow_html=True
    )

    delete_type = st.selectbox(
        "Transaction type",
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
            "No transactions available for this type."
        )

    else:

        delete_labels = {}

        for row in delete_options:

            delete_labels[
                f"{row[3]} | {row[1]} | ₹{row[2]:,.2f}"
            ] = row[0]

        selected_transaction = st.selectbox(
            "Select transaction to remove",
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


# =========================================================
# SPENDING ANALYSIS
# =========================================================

elif page == "Spending Analysis":

    st.markdown(
        '<div class="page-eyebrow">Analytics</div>',
        unsafe_allow_html=True
    )

    st.title("Spending Analysis")

    st.markdown(
        """
        <div class="page-description">
            Understand your spending patterns and identify the categories
            that have the biggest impact on your finances.
        </div>
        """,
        unsafe_allow_html=True
    )

    if len(expenses) == 0:

        st.info(
            "Add expenses to generate your spending analysis."
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

        highest_category = max(
            category_totals,
            key=category_totals.get
        )

        highest_amount = (
            category_totals[
                highest_category
            ]
        )

        highest_percentage = (
            category_percentages[
                highest_category
            ]
        )

        # -----------------------------------------
        # KPI Cards
        # -----------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">
                        Total Spending
                    </div>

                    <div class="metric-value">
                        ₹{total_expenses:,.0f}
                    </div>

                    <div class="metric-small">
                        All recorded expenses
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">
                        Largest Category
                    </div>

                    <div class="metric-value">
                        {highest_category}
                    </div>

                    <div class="metric-small">
                        ₹{highest_amount:,.0f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">
                        Category Share
                    </div>

                    <div class="metric-value">
                        {highest_percentage:.1f}%
                    </div>

                    <div class="metric-small">
                        Of total spending
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")

        # -----------------------------------------
        # Charts
        # -----------------------------------------

        col1, col2 = st.columns([1.4, 1])

        with col1:

            st.markdown(
                '<div class="section-label">Spending by Category</div>',
                unsafe_allow_html=True
            )

            spending_df = pd.DataFrame(
                {
                    "Amount": category_totals
                }
            )

            st.bar_chart(
                spending_df,
                height=360
            )

        with col2:

            st.markdown(
                '<div class="section-label">Category Distribution</div>',
                unsafe_allow_html=True
            )

            breakdown_df = pd.DataFrame(
                {
                    "Category": list(
                        category_percentages.keys()
                    ),
                    "Share": list(
                        category_percentages.values()
                    )
                }
            )

            breakdown_df = breakdown_df.sort_values(
                "Share",
                ascending=False
            )

            st.dataframe(
                breakdown_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Share": st.column_config.ProgressColumn(
                        "Share",
                        format="%.1f%%",
                        min_value=0,
                        max_value=100
                    )
                }
            )

        st.divider()

        # -----------------------------------------
        # Spending Insight
        # -----------------------------------------

        if highest_percentage >= 50:

            insight = (
                f"{highest_category} represents "
                f"{highest_percentage:.1f}% of your spending. "
                "This category is worth reviewing for possible "
                "savings opportunities."
            )

        elif highest_percentage >= 30:

            insight = (
                f"{highest_category} is your largest spending "
                f"category at {highest_percentage:.1f}%. "
                "Keep monitoring this category."
            )

        else:

            insight = (
                "Your spending is relatively distributed "
                "across multiple categories."
            )

        st.markdown(
            f"""
            <div class="insight-card">

                <div class="insight-label">
                    Spending Insight
                </div>

                <div class="insight-text">
                    {insight}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# CALCULATORS
# =========================================================

elif page == "Calculators":

    st.markdown(
        '<div class="page-eyebrow">Financial tools</div>',
        unsafe_allow_html=True
    )

    st.title("Financial Calculators")

    st.markdown(
        """
        <div class="page-description">
            Calculate interest, SIP returns and loan payments.
        </div>
        """,
        unsafe_allow_html=True
    )

    calculator = st.selectbox(
        "Select calculator",
        [
            "Simple Interest",
            "Compound Interest",
            "SIP Calculator",
            "EMI Calculator"
        ]
    )

    st.divider()

    # -----------------------------------------
    # Simple Interest
    # -----------------------------------------

    if calculator == "Simple Interest":

        st.subheader("Simple Interest")

        col1, col2 = st.columns(2)

        with col1:

            principal = st.number_input(
                "Principal amount",
                min_value=0.0,
                step=1000.0
            )

            rate = st.number_input(
                "Annual interest rate (%)",
                min_value=0.0,
                step=0.5
            )

        with col2:

            years = st.number_input(
                "Time in years",
                min_value=0.1,
                step=1.0
            )

        if st.button(
            "Calculate",
            type="primary"
        ):

            interest, amount = (
                calculate_simple_interest(
                    principal,
                    rate,
                    years
                )
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Interest",
                    f"₹{interest:,.2f}"
                )

            with col2:

                st.metric(
                    "Total Amount",
                    f"₹{amount:,.2f}"
                )

    # -----------------------------------------
    # Compound Interest
    # -----------------------------------------

    elif calculator == "Compound Interest":

        st.subheader("Compound Interest")

        col1, col2 = st.columns(2)

        with col1:

            principal = st.number_input(
                "Principal amount",
                min_value=0.0,
                step=1000.0
            )

            rate = st.number_input(
                "Annual interest rate (%)",
                min_value=0.0,
                step=0.5
            )

        with col2:

            years = st.number_input(
                "Time in years",
                min_value=0.1,
                step=1.0
            )

            compounds = st.number_input(
                "Compounds per year",
                min_value=1,
                step=1
            )

        if st.button(
            "Calculate",
            type="primary"
        ):

            interest, amount = (
                calculate_compound_interest(
                    principal,
                    rate,
                    years,
                    compounds
                )
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Interest",
                    f"₹{interest:,.2f}"
                )

            with col2:

                st.metric(
                    "Total Amount",
                    f"₹{amount:,.2f}"
                )

    # -----------------------------------------
    # SIP
    # -----------------------------------------

    elif calculator == "SIP Calculator":

        st.subheader("SIP Calculator")

        col1, col2 = st.columns(2)

        with col1:

            monthly_investment = st.number_input(
                "Monthly investment",
                min_value=0.0,
                step=500.0
            )

            annual_rate = st.number_input(
                "Expected annual return (%)",
                min_value=0.0,
                step=0.5
            )

        with col2:

            years = st.number_input(
                "Investment period",
                min_value=0.1,
                step=1.0
            )

        if st.button(
            "Calculate",
            type="primary"
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

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Total Invested",
                    f"₹{total_invested:,.2f}"
                )

            with col2:

                st.metric(
                    "Estimated Returns",
                    f"₹{estimated_returns:,.2f}"
                )

            with col3:

                st.metric(
                    "Estimated Value",
                    f"₹{final_value:,.2f}"
                )

    # -----------------------------------------
    # EMI
    # -----------------------------------------

    elif calculator == "EMI Calculator":

        st.subheader("EMI Calculator")

        col1, col2 = st.columns(2)

        with col1:

            principal = st.number_input(
                "Loan amount",
                min_value=0.0,
                step=5000.0
            )

            annual_rate = st.number_input(
                "Annual interest rate (%)",
                min_value=0.0,
                step=0.5
            )

        with col2:

            years = st.number_input(
                "Loan period",
                min_value=0.1,
                step=1.0
            )

        if st.button(
            "Calculate",
            type="primary"
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

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Monthly EMI",
                    f"₹{emi:,.2f}"
                )

            with col2:

                st.metric(
                    "Total Interest",
                    f"₹{total_interest:,.2f}"
                )

            with col3:

                st.metric(
                    "Total Payment",
                    f"₹{total_payment:,.2f}"
                )


# =========================================================
# AI FINANCIAL ADVISOR
# =========================================================

elif page == "AI Financial Advisor":

    st.markdown(
        '<div class="page-eyebrow">Artificial intelligence</div>',
        unsafe_allow_html=True
    )

    st.title("AI Financial Advisor")

    st.markdown(
        """
        <div class="page-description">
            Generate personalized financial insights using your recorded
            income and spending data.
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------
    # Financial Snapshot
    # -----------------------------------------

    st.markdown(
        '<div class="section-label">Financial Snapshot</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Income",
            f"₹{total_income:,.0f}"
        )

    with col2:

        st.metric(
            "Expenses",
            f"₹{total_expenses:,.0f}"
        )

    with col3:

        st.metric(
            "Balance",
            f"₹{balance:,.0f}"
        )

    with col4:

        st.metric(
            "Savings Rate",
            f"{savings_rate:.1f}%"
        )

    st.divider()

    (
        highest_category,
        highest_amount
    ) = find_highest_spending_category(
        expenses
    )

    if highest_category is not None:

        st.markdown(
            f"""
            <div class="content-card">

                <div class="card-title">
                    Current Spending Focus
                </div>

                <div class="card-subtitle">
                    Highest recorded expense category
                </div>

                <div style="
                    font-size:1.5rem;
                    font-weight:700;
                    color:#f0f3f6;
                ">
                    {highest_category}
                </div>

                <div style="
                    color:#8b97a5;
                    margin-top:0.35rem;
                ">
                    ₹{highest_amount:,.2f}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # -----------------------------------------
    # AI Button
    # -----------------------------------------

    if st.button(
        "Generate Financial Analysis",
        type="primary",
        use_container_width=True
    ):

        if total_income == 0 and total_expenses == 0:

            st.warning(
                "Add some income and expenses before generating AI analysis."
            )

        else:

            prompt = create_financial_prompt(
                total_income,
                total_expenses,
                balance,
                savings_rate,
                highest_category,
                highest_amount
            )

            with st.spinner(
                "Analyzing your financial data..."
            ):

                try:

                    advice = get_ai_financial_advice(
                        prompt
                    )

                    st.success(
                        "Financial analysis completed."
                    )

                    st.markdown(
                        '<div class="section-label">AI Analysis</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <div class="insight-card">
                            <div class="insight-text">
                                {advice}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                except Exception as error:

                    st.error(
                        "Unable to generate AI analysis at the moment."
                    )

                    st.caption(
                        f"Technical error: {error}"
                    )