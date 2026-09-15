import streamlit as st
from datetime import date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    calculate_category_totals
)

from financial_insights import (
    generate_financial_insights
)

from financial_health import (
    calculate_financial_health_score
)

from budget import (
    calculate_budget_status,
    calculate_total_budget,
    calculate_total_spending,
    calculate_remaining_budget
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
    delete_expense,
    save_budget,
    get_budgets,
    delete_budget
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Finance Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 15% 0%,
                rgba(79, 70, 229, 0.10),
                transparent 25%
            ),
            radial-gradient(
                circle at 90% 5%,
                rgba(16, 185, 129, 0.07),
                transparent 25%
            ),
            #080d19;
        color: #f8fafc;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0c1324 0%,
                #080d19 100%
            );
        border-right: 1px solid #1c2940;
    }

    section[data-testid="stSidebar"] * {
        color: #e2e8f0;
    }

    section[data-testid="stSidebar"] .stRadio label {
        font-weight: 500;
    }

    .main-title {
        font-size: 2.35rem;
        font-weight: 800;
        letter-spacing: -1.3px;
        line-height: 1.15;
        margin-bottom: 7px;
    }

    .subtitle {
        color: #8fa0b8;
        font-size: 0.98rem;
        line-height: 1.6;
        margin-bottom: 1.8rem;
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 750;
        letter-spacing: -0.2px;
        margin-top: 30px;
        margin-bottom: 14px;
    }

    .welcome-card {
        position: relative;
        overflow: hidden;
        background:
            linear-gradient(
                135deg,
                rgba(30, 41, 75, 0.95),
                rgba(14, 22, 39, 0.98)
            );
        border: 1px solid #273652;
        border-radius: 22px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow:
            0 15px 45px rgba(0, 0, 0, 0.20);
    }

    .welcome-card:before {
        content: "";
        position: absolute;
        width: 240px;
        height: 240px;
        right: -80px;
        top: -100px;
        border-radius: 50%;
        background:
            radial-gradient(
                circle,
                rgba(99, 102, 241, 0.25),
                transparent 65%
            );
    }

    .welcome-card:after {
        content: "";
        position: absolute;
        width: 130px;
        height: 130px;
        right: 90px;
        bottom: -90px;
        border-radius: 50%;
        background:
            radial-gradient(
                circle,
                rgba(16, 185, 129, 0.13),
                transparent 65%
            );
    }

    .welcome-title {
        position: relative;
        z-index: 2;
        font-size: 1.55rem;
        font-weight: 800;
        letter-spacing: -0.4px;
        margin-bottom: 7px;
    }

    .welcome-text {
        position: relative;
        z-index: 2;
        color: #a7b4c8;
        font-size: 0.94rem;
        line-height: 1.6;
        max-width: 800px;
    }

    .metric-card {
        background:
            linear-gradient(
                145deg,
                rgba(17, 27, 46, 0.98),
                rgba(11, 18, 32, 0.98)
            );
        border: 1px solid #22304a;
        border-radius: 18px;
        padding: 21px 20px;
        min-height: 126px;
        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.14);
        transition:
            transform 0.2s ease,
            border-color 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #344563;
    }

    .metric-label {
        color: #8292aa;
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.8px;
        margin-bottom: 10px;
    }

    .metric-value {
        font-size: 1.55rem;
        font-weight: 800;
        letter-spacing: -0.4px;
    }

    .metric-subtitle {
        color: #687991;
        font-size: 0.76rem;
        margin-top: 7px;
    }

    .metric-positive {
        color: #34d399;
    }

    .metric-negative {
        color: #fb7185;
    }

    .metric-blue {
        color: #60a5fa;
    }

    .metric-purple {
        color: #a78bfa;
    }

    .health-card {
        background:
            linear-gradient(
                145deg,
                rgba(13, 53, 48, 0.62),
                rgba(12, 24, 36, 0.96)
            );
        border: 1px solid rgba(52, 211, 153, 0.22);
        border-radius: 20px;
        padding: 22px;
        min-height: 150px;
    }

    .health-score {
        font-size: 2.35rem;
        font-weight: 850;
        letter-spacing: -1px;
        margin: 4px 0;
    }

    .health-label {
        color: #34d399;
        font-size: 0.88rem;
        font-weight: 700;
    }

    .health-description {
        color: #8fa0b8;
        font-size: 0.82rem;
        line-height: 1.5;
        margin-top: 9px;
    }

    .insight-card {
        background:
            linear-gradient(
                145deg,
                rgba(23, 34, 54, 0.92),
                rgba(14, 23, 38, 0.95)
            );
        border: 1px solid #263650;
        border-radius: 17px;
        padding: 17px 19px;
        margin-bottom: 11px;
        box-shadow:
            0 7px 22px rgba(0, 0, 0, 0.12);
    }

    .insight-title {
        color: #e2e8f0;
        font-weight: 750;
        margin-bottom: 6px;
    }

    .insight-text {
        color: #aab7c9;
        font-size: 0.91rem;
        line-height: 1.6;
    }

    .alert-card {
        background:
            linear-gradient(
                145deg,
                rgba(91, 31, 43, 0.32),
                rgba(38, 19, 29, 0.42)
            );
        border: 1px solid rgba(248, 113, 113, 0.25);
        border-radius: 17px;
        padding: 17px 19px;
        margin-bottom: 11px;
    }

    .trend-card {
        background:
            linear-gradient(
                145deg,
                rgba(17, 27, 46, 0.97),
                rgba(11, 18, 32, 0.97)
            );
        border: 1px solid #22304a;
        border-radius: 17px;
        padding: 18px 19px;
        min-height: 105px;
    }

    .trend-label {
        color: #8292aa;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.7px;
    }

    .trend-value {
        color: #f8fafc;
        font-size: 1.35rem;
        font-weight: 800;
        margin: 6px 0 3px;
    }

    .budget-card {
        background:
            linear-gradient(
                145deg,
                rgba(17, 27, 46, 0.98),
                rgba(11, 18, 32, 0.98)
            );
        border: 1px solid #22304a;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 12px;
    }

    .budget-category {
        font-size: 1rem;
        font-weight: 750;
        color: #f8fafc;
        margin-bottom: 5px;
    }

    .budget-details {
        color: #8292aa;
        font-size: 0.82rem;
    }

    .budget-snapshot {
        background:
            linear-gradient(
                145deg,
                rgba(24, 37, 64, 0.98),
                rgba(11, 18, 32, 0.98)
            );
        border: 1px solid #2a3c5c;
        border-radius: 20px;
        padding: 22px;
        margin-bottom: 15px;
    }

    .budget-status {
        color: #94a3b8;
        font-size: 0.82rem;
        margin-top: 6px;
    }

    .stButton > button {
        border-radius: 11px;
        border: 1px solid #33445f;
        background:
            linear-gradient(
                135deg,
                #1b2942,
                #111b2e
            );
        color: #f8fafc;
        font-weight: 650;
        min-height: 42px;
        transition:
            transform 0.15s ease,
            border-color 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        border-color: #64748b;
        color: #ffffff;
    }

    div[data-baseweb="select"] > div {
        background-color: #111a2b;
        border-color: #263650;
        border-radius: 10px;
    }

    div[data-baseweb="input"] > div {
        background-color: #111a2b;
        border-color: #263650;
        border-radius: 10px;
    }

    textarea {
        background-color: #111a2b !important;
        border-color: #263650 !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #22304a;
        border-radius: 15px;
        overflow: hidden;
    }

    div[data-testid="stAlert"] {
        border-radius: 13px;
    }

    div[data-testid="stProgressBar"] {
        margin-top: 12px;
        margin-bottom: 10px;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DATABASE DATA CONVERSION
# =========================================================

def load_income():

    raw_income = get_all_income()

    income_records = []

    for record in raw_income:

        if isinstance(record, dict):

            income_records.append(record)

        elif isinstance(record, (tuple, list)):

            if len(record) >= 4:

                income_records.append(
                    {
                        "id": record[0],
                        "source": record[1],
                        "amount": float(record[2]),
                        "date": record[3]
                    }
                )

    return income_records


def load_expenses():

    raw_expenses = get_all_expenses()

    expense_records = []

    for record in raw_expenses:

        if isinstance(record, dict):

            expense_records.append(record)

        elif isinstance(record, (tuple, list)):

            if len(record) >= 4:

                expense_records.append(
                    {
                        "id": record[0],
                        "category": record[1],
                        "amount": float(record[2]),
                        "date": record[3]
                    }
                )

    return expense_records


# =========================================================
# GENERAL HELPERS
# =========================================================

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
            balance /
            total_income
        ) * 100

    else:

        savings_rate = 0

    return (
        total_income,
        total_expenses,
        balance,
        savings_rate
    )


def format_currency(value):

    return f"₹{value:,.2f}"


def filter_by_month(records, selected_month):

    if selected_month == "All Time":

        return records

    filtered = []

    for record in records:

        record_date = record.get("date")

        if record_date:

            if str(record_date)[:7] == selected_month:

                filtered.append(record)

    return filtered


def get_available_months(incomes, expenses):

    months = set()

    for record in incomes + expenses:

        record_date = record.get("date")

        if record_date:

            months.add(
                str(record_date)[:7]
            )

    return sorted(
        months,
        reverse=True
    )


def get_budget_months():

    budget_months = set()

    try:

        all_budgets = get_budgets()

        for row in all_budgets:

            if isinstance(row, (tuple, list)):

                if len(row) >= 4:

                    month = row[3]

                    if month:

                        budget_months.add(
                            str(month)[:7]
                        )

    except Exception:

        pass

    return budget_months


def get_combined_available_months(
    incomes,
    expenses
):

    transaction_months = set(
        get_available_months(
            incomes,
            expenses
        )
    )

    budget_months = get_budget_months()

    current_month = date.today().strftime(
        "%Y-%m"
    )

    all_months = (
        transaction_months |
        budget_months |
        {current_month}
    )

    return sorted(
        all_months,
        reverse=True
    )


def month_display(month):

    if month == "All Time":

        return "All Time"

    try:

        return pd.to_datetime(
            month + "-01"
        ).strftime(
            "%B %Y"
        )

    except Exception:

        return month


def get_previous_month(selected_month):

    if selected_month == "All Time":

        return None

    try:

        current = pd.to_datetime(
            selected_month + "-01"
        )

        previous = (
            current -
            pd.DateOffset(months=1)
        )

        return previous.strftime(
            "%Y-%m"
        )

    except Exception:

        return None


def get_month_totals(
    incomes,
    expenses,
    month
):

    month_income = filter_by_month(
        incomes,
        month
    )

    month_expenses = filter_by_month(
        expenses,
        month
    )

    income = sum(
        item["amount"]
        for item in month_income
    )

    expenses_total = sum(
        item["amount"]
        for item in month_expenses
    )

    return (
        income,
        expenses_total
    )


# =========================================================
# BUDGET HELPERS
# =========================================================

def get_budget_data_for_month(
    selected_month,
    expenses
):

    if selected_month == "All Time":

        return None

    budget_rows = get_budgets(
        selected_month
    )

    category_budgets = {}

    for row in budget_rows:

        if isinstance(row, (tuple, list)):

            if len(row) >= 4:

                category = row[1]
                amount = float(row[2])

                category_budgets[
                    category
                ] = amount

    month_expenses = filter_by_month(
        expenses,
        selected_month
    )

    category_totals = calculate_category_totals(
        month_expenses
    )

    if not category_budgets:

        return None

    total_budget = calculate_total_budget(
        category_budgets
    )

    total_spending = calculate_total_spending(
        category_totals
    )

    remaining_budget = calculate_remaining_budget(
        total_budget,
        total_spending
    )

    if total_budget > 0:

        budget_used_percentage = (
            total_spending /
            total_budget
        ) * 100

    else:

        budget_used_percentage = 0

    budget_status = calculate_budget_status(
        category_budgets,
        category_totals
    )

    if total_spending > total_budget:

        overall_status = "Over Budget"

    elif budget_used_percentage >= 80:

        overall_status = "Almost Reached"

    else:

        overall_status = "Within Budget"

    return {
        "budget_rows": budget_rows,
        "category_budgets": category_budgets,
        "category_totals": category_totals,
        "total_budget": total_budget,
        "total_spending": total_spending,
        "remaining_budget": remaining_budget,
        "budget_used_percentage": budget_used_percentage,
        "budget_status": budget_status,
        "overall_status": overall_status
    }


def create_budget_snapshot_chart(
    category_budgets,
    category_totals
):

    chart_rows = []

    for category in category_budgets:

        chart_rows.append(
            {
                "Category": category,
                "Budget": category_budgets[
                    category
                ],
                "Actual Spending": category_totals.get(
                    category,
                    0
                )
            }
        )

    if not chart_rows:

        return None

    budget_df = pd.DataFrame(
        chart_rows
    )

    budget_long = budget_df.melt(
        id_vars="Category",
        value_vars=[
            "Budget",
            "Actual Spending"
        ],
        var_name="Type",
        value_name="Amount"
    )

    fig = px.bar(
        budget_long,
        x="Category",
        y="Amount",
        color="Type",
        barmode="group",
        text="Amount"
    )

    fig.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside"
    )

    fig.update_layout(
        title="Budget vs Actual Spending",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#dbe5f2"
        ),

        yaxis=dict(
            gridcolor="#202d43",
            zeroline=False
        ),

        margin=dict(
            l=20,
            r=20,
            t=55,
            b=20
        ),

        legend=dict(
            orientation="h",
            y=1.08,
            x=0
        )
    )

    return fig


# =========================================================
# CHART FUNCTIONS
# =========================================================

def create_financial_chart(
    income,
    expenses
):

    data = pd.DataFrame(
        {
            "Type": [
                "Income",
                "Expenses"
            ],
            "Amount": [
                income,
                expenses
            ]
        }
    )

    fig = px.bar(
        data,
        x="Type",
        y="Amount",
        text="Amount"
    )

    fig.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside"
    )

    fig.update_layout(
        title="Income vs Expenses",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#dbe5f2"
        ),

        yaxis=dict(
            gridcolor="#202d43",
            zeroline=False
        ),

        xaxis=dict(
            title=""
        ),

        margin=dict(
            l=20,
            r=20,
            t=55,
            b=20
        ),

        showlegend=False
    )

    return fig


def create_spending_chart(expenses):

    category_totals = (
        calculate_category_totals(
            expenses
        )
    )

    if not category_totals:

        return None

    data = pd.DataFrame(
        {
            "Category": list(
                category_totals.keys()
            ),

            "Amount": list(
                category_totals.values()
            )
        }
    )

    fig = px.pie(
        data,
        names="Category",
        values="Amount",
        hole=0.58
    )

    fig.update_layout(
        title="Spending Breakdown",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#dbe5f2"
        ),

        margin=dict(
            l=10,
            r=10,
            t=55,
            b=10
        ),

        legend=dict(
            orientation="h",
            y=-0.08
        )
    )

    return fig


def create_trend_chart(
    incomes,
    expenses
):

    monthly_data = {}

    for income in incomes:

        month = str(
            income.get(
                "date",
                ""
            )
        )[:7]

        if month:

            if month not in monthly_data:

                monthly_data[month] = {
                    "Income": 0,
                    "Expenses": 0
                }

            monthly_data[month]["Income"] += (
                income["amount"]
            )

    for expense in expenses:

        month = str(
            expense.get(
                "date",
                ""
            )
        )[:7]

        if month:

            if month not in monthly_data:

                monthly_data[month] = {
                    "Income": 0,
                    "Expenses": 0
                }

            monthly_data[month]["Expenses"] += (
                expense["amount"]
            )

    if not monthly_data:

        return None

    rows = []

    for month in sorted(monthly_data):

        rows.append(
            {
                "Month": month,
                "Income": monthly_data[month]["Income"],
                "Expenses": monthly_data[month]["Expenses"]
            }
        )

    data = pd.DataFrame(rows)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["Month"],
            y=data["Income"],
            mode="lines+markers",
            name="Income"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data["Month"],
            y=data["Expenses"],
            mode="lines+markers",
            name="Expenses"
        )
    )

    fig.update_layout(
        title="Monthly Financial Trend",

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#dbe5f2"
        ),

        yaxis=dict(
            gridcolor="#202d43",
            zeroline=False
        ),

        margin=dict(
            l=20,
            r=20,
            t=55,
            b=20
        ),

        legend=dict(
            orientation="h",
            y=1.08,
            x=0
        )
    )

    return fig


# =========================================================
# LOAD APPLICATION DATA
# =========================================================

incomes = load_income()

expenses = load_expenses()

available_months = get_combined_available_months(
    incomes,
    expenses
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <div style="
        padding: 8px 4px 20px 4px;
    ">

        <div style="
            font-size:1.45rem;
            font-weight:850;
            letter-spacing:-0.5px;
        ">
            💼 AI Finance
        </div>

        <div style="
            color:#72839c;
            font-size:0.78rem;
            margin-top:5px;
            line-height:1.5;
        ">
            Personal Financial Intelligence
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


page = st.sidebar.radio(
    "WORKSPACE",
    [
        "Dashboard",
        "Add Transaction",
        "History",
        "Spending Analysis",
        "Budget Planner",
        "Calculators",
        "AI Financial Advisor"
    ]
)


st.sidebar.markdown("---")


st.sidebar.markdown(
    """
    <div style="
        padding:5px 3px;
        color:#667993;
        font-size:0.73rem;
        line-height:1.7;
    ">
        <b style="color:#94a3b8;">
            AI FINANCE ASSISTANT
        </b>
        <br>
        Python · Streamlit · SQLite · AI
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.markdown(
        '<div class="main-title">'
        'Financial Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'A clear view of your income, spending, savings '
        'and financial health.'
        '</div>',
        unsafe_allow_html=True
    )

    month_options = (
        ["All Time"] +
        available_months
    )

    selected_month = st.selectbox(
        "Analysis period",
        month_options,
        format_func=month_display
    )

    current_incomes = filter_by_month(
        incomes,
        selected_month
    )

    current_expenses = filter_by_month(
        expenses,
        selected_month
    )

    total_income = sum(
        item["amount"]
        for item in current_incomes
    )

    total_expenses = sum(
        item["amount"]
        for item in current_expenses
    )

    balance = (
        total_income -
        total_expenses
    )

    if total_income > 0:

        savings_rate = (
            balance /
            total_income
        ) * 100

    else:

        savings_rate = 0

    expense_ratio = (
        total_expenses /
        total_income *
        100
        if total_income > 0
        else 0
    )

    if balance > 0:

        message = (
            "You're spending less than you earn. "
            "Your current cash position is positive — "
            "keep building that financial momentum."
        )

    elif balance == 0:

        message = (
            "Your income and expenses are currently balanced. "
            "Use the insights below to identify opportunities "
            "to improve your savings."
        )

    else:

        message = (
            "Your expenses are higher than your income. "
            "Review your spending categories and identify "
            "where adjustments may be possible."
        )

    st.markdown(
        f"""
        <div class="welcome-card">

            <div class="welcome-title">
                Your money, clearly understood.
            </div>

            <div class="welcome-text">
                {message}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    TOTAL INCOME
                </div>

                <div class="metric-value metric-positive">
                    {format_currency(total_income)}
                </div>

                <div class="metric-subtitle">
                    Money received
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
                    TOTAL EXPENSES
                </div>

                <div class="metric-value metric-negative">
                    {format_currency(total_expenses)}
                </div>

                <div class="metric-subtitle">
                    Money spent
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        balance_class = (
            "metric-positive"
            if balance >= 0
            else "metric-negative"
        )

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    REMAINING BALANCE
                </div>

                <div class="metric-value {balance_class}">
                    {format_currency(balance)}
                </div>

                <div class="metric-subtitle">
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

                <div class="metric-label">
                    SAVINGS RATE
                </div>

                <div class="metric-value metric-purple">
                    {savings_rate:.1f}%
                </div>

                <div class="metric-subtitle">
                    Percentage retained
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # BUDGET SNAPSHOT — STEP 5
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🎯 Budget Snapshot'
        '</div>',
        unsafe_allow_html=True
    )

    budget_snapshot = get_budget_data_for_month(
        selected_month,
        expenses
    )

    if selected_month == "All Time":

        st.info(
            "Select a specific month to view its Budget Snapshot."
        )

    elif budget_snapshot is None:

        st.info(
            f"No budget has been created for "
            f"{month_display(selected_month)} yet. "
            "Go to Budget Planner to set monthly spending limits."
        )

    else:

        snapshot_budget = budget_snapshot[
            "total_budget"
        ]

        snapshot_spending = budget_snapshot[
            "total_spending"
        ]

        snapshot_remaining = budget_snapshot[
            "remaining_budget"
        ]

        snapshot_percentage = budget_snapshot[
            "budget_used_percentage"
        ]

        snapshot_status = budget_snapshot[
            "overall_status"
        ]

        budget_col1, budget_col2, budget_col3, budget_col4 = (
            st.columns(4)
        )

        with budget_col1:

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        TOTAL BUDGET
                    </div>

                    <div class="metric-value metric-blue">
                        {format_currency(snapshot_budget)}
                    </div>

                    <div class="metric-subtitle">
                        Planned monthly spending
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with budget_col2:

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        ACTUAL SPENDING
                    </div>

                    <div class="metric-value metric-negative">
                        {format_currency(snapshot_spending)}
                    </div>

                    <div class="metric-subtitle">
                        Recorded expenses
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with budget_col3:

            remaining_class = (
                "metric-positive"
                if snapshot_remaining >= 0
                else "metric-negative"
            )

            remaining_text = (
                format_currency(snapshot_remaining)
                if snapshot_remaining >= 0
                else "-" +
                format_currency(
                    abs(snapshot_remaining)
                )
            )

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        REMAINING BUDGET
                    </div>

                    <div class="metric-value {remaining_class}">
                        {remaining_text}
                    </div>

                    <div class="metric-subtitle">
                        Budget minus spending
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with budget_col4:

            if snapshot_percentage > 100:

                percentage_display = (
                    f"{snapshot_percentage:.1f}%"
                )

            else:

                percentage_display = (
                    f"{snapshot_percentage:.1f}%"
                )

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        BUDGET USED
                    </div>

                    <div class="metric-value metric-purple">
                        {percentage_display}
                    </div>

                    <div class="metric-subtitle">
                        Of planned budget
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        progress_value = min(
            snapshot_percentage / 100,
            1.0
        )

        st.progress(
            progress_value
        )

        if snapshot_status == "Over Budget":

            st.error(
                f"⚠️ You are over budget by "
                f"{format_currency(abs(snapshot_remaining))}."
            )

        elif snapshot_status == "Almost Reached":

            st.warning(
                f"⚠️ You have used {snapshot_percentage:.1f}% "
                f"of your monthly budget. "
                f"{format_currency(max(snapshot_remaining, 0))} remains."
            )

        else:

            st.success(
                f"✓ Your spending is within budget. "
                f"{format_currency(max(snapshot_remaining, 0))} remains."
            )

        snapshot_chart = create_budget_snapshot_chart(
            budget_snapshot["category_budgets"],
            budget_snapshot["category_totals"]
        )

        if snapshot_chart:

            st.plotly_chart(
                snapshot_chart,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

    # -----------------------------------------------------
    # FINANCIAL HEALTH
    # -----------------------------------------------------

    health_score, health_label = (
        calculate_financial_health_score(
            total_income,
            total_expenses,
            savings_rate
        )
    )

    st.markdown(
        '<div class="section-title">'
        'Financial Health'
        '</div>',
        unsafe_allow_html=True
    )

    health_col1, health_col2 = st.columns(
        [1, 2]
    )

    with health_col1:

        st.markdown(
            f"""
            <div class="health-card">

                <div style="
                    color:#7f91aa;
                    font-size:0.72rem;
                    font-weight:700;
                    letter-spacing:0.8px;
                ">
                    FINANCIAL HEALTH SCORE
                </div>

                <div class="health-score">
                    {health_score}/100
                </div>

                <div class="health-label">
                    {health_label}
                </div>

                <div class="health-description">
                    Based on your savings performance,
                    spending level and remaining balance.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with health_col2:

        st.progress(
            health_score / 100
        )

        st.caption(
            "Your score is calculated from the financial "
            "data recorded in the application."
        )

        if health_score >= 80:

            st.success(
                "Your current financial indicators are strong. "
                "Continue maintaining healthy savings and spending habits."
            )

        elif health_score >= 60:

            st.info(
                "Your financial position is generally healthy, "
                "with some room for improvement."
            )

        elif health_score >= 40:

            st.warning(
                "Your financial position is moderate. "
                "Improving savings and controlling expenses could help."
            )

        elif health_score >= 20:

            st.warning(
                "Your finances need attention. "
                "Review your spending and try to increase your savings."
            )

        else:

            st.error(
                "Your current financial indicators are under pressure. "
                "Consider reviewing expenses carefully."
            )

    # -----------------------------------------------------
    # FINANCIAL INTELLIGENCE
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🧠 Financial Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    previous_month = get_previous_month(
        selected_month
    )

    if previous_month:

        previous_income, previous_expenses = (
            get_month_totals(
                incomes,
                expenses,
                previous_month
            )
        )

        intelligence = (
            generate_financial_insights(
                current_income=total_income,
                current_expenses=total_expenses,
                previous_income=previous_income,
                previous_expenses=previous_expenses,
                expenses=current_expenses
            )
        )

        t1, t2, t3 = st.columns(3)

        with t1:

            income_change = intelligence[
                "income_change"
            ]

            symbol = (
                "↑"
                if income_change > 0
                else "↓"
                if income_change < 0
                else "→"
            )

            st.markdown(
                f"""
                <div class="trend-card">

                    <div class="trend-label">
                        INCOME TREND
                    </div>

                    <div class="trend-value">
                        {symbol} {abs(income_change):.1f}%
                    </div>

                    <div class="trend-label">
                        vs previous month
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with t2:

            expense_change = intelligence[
                "expense_change"
            ]

            symbol = (
                "↑"
                if expense_change > 0
                else "↓"
                if expense_change < 0
                else "→"
            )

            st.markdown(
                f"""
                <div class="trend-card">

                    <div class="trend-label">
                        EXPENSE TREND
                    </div>

                    <div class="trend-value">
                        {symbol} {abs(expense_change):.1f}%
                    </div>

                    <div class="trend-label">
                        vs previous month
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with t3:

            savings_change = intelligence[
                "savings_change"
            ]

            symbol = (
                "↑"
                if savings_change > 0
                else "↓"
                if savings_change < 0
                else "→"
            )

            st.markdown(
                f"""
                <div class="trend-card">

                    <div class="trend-label">
                        SAVINGS TREND
                    </div>

                    <div class="trend-value">
                        {symbol} {abs(savings_change):.1f}%
                    </div>

                    <div class="trend-label">
                        vs previous month
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        if intelligence["alerts"]:

            st.markdown(
                "#### 🚨 Financial Alerts"
            )

            for alert in intelligence["alerts"]:

                st.markdown(
                    f"""
                    <div class="alert-card">

                        <div class="insight-title">
                            ⚠️ Attention
                        </div>

                        <div class="insight-text">
                            {alert}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        if intelligence["insights"]:

            st.markdown(
                "#### 💡 Smart Insights"
            )

            for insight in intelligence["insights"]:

                st.markdown(
                    f"""
                    <div class="insight-card">

                        <div class="insight-title">
                            ✦ Financial Insight
                        </div>

                        <div class="insight-text">
                            {insight}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:

        st.info(
            "Select a specific month to compare it with "
            "the previous month and unlock Financial Intelligence."
        )

    # -----------------------------------------------------
    # MONEY OVERVIEW
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Money Overview'
        '</div>',
        unsafe_allow_html=True
    )

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        fig = create_financial_chart(
            total_income,
            total_expenses
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    with chart_col2:

        spending_fig = create_spending_chart(
            current_expenses
        )

        if spending_fig:

            st.plotly_chart(
                spending_fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        else:

            st.info(
                "Add expenses to see your spending breakdown."
            )

    # -----------------------------------------------------
    # SPENDING EXPLORER
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🔎 Spending Explorer'
        '</div>',
        unsafe_allow_html=True
    )

    category_totals = (
        calculate_category_totals(
            current_expenses
        )
    )

    if category_totals:

        selected_category = st.selectbox(
            "Explore a spending category",
            list(
                category_totals.keys()
            )
        )

        category_amount = (
            category_totals[
                selected_category
            ]
        )

        if total_expenses > 0:

            category_percentage = (
                category_amount /
                total_expenses
            ) * 100

        else:

            category_percentage = 0

        e1, e2, e3 = st.columns(3)

        with e1:

            st.metric(
                "Category Spending",
                format_currency(
                    category_amount
                )
            )

        with e2:

            st.metric(
                "Share of Expenses",
                f"{category_percentage:.1f}%"
            )

        with e3:

            if category_percentage >= 50:

                status = "High"

            elif category_percentage >= 30:

                status = "Significant"

            else:

                status = "Controlled"

            st.metric(
                "Spending Level",
                status
            )

    else:

        st.info(
            "Add expenses to explore your spending categories."
        )

    # -----------------------------------------------------
    # FINANCIAL TREND
    # -----------------------------------------------------

    trend_fig = create_trend_chart(
        incomes,
        expenses
    )

    if trend_fig:

        st.markdown(
            '<div class="section-title">'
            '📈 Financial Trend'
            '</div>',
            unsafe_allow_html=True
        )

        st.plotly_chart(
            trend_fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    # -----------------------------------------------------
    # MONEY STORY
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Your Money Story'
        '</div>',
        unsafe_allow_html=True
    )

    if (
        total_income == 0
        and
        total_expenses == 0
    ):

        st.info(
            "Start by adding your income and expenses. "
            "Your financial story will appear here."
        )

    elif balance > 0:

        st.success(
            f"You earned "
            f"{format_currency(total_income)} "
            f"and spent "
            f"{format_currency(total_expenses)}. "
            f"You currently have "
            f"{format_currency(balance)} remaining."
        )

    else:

        st.warning(
            f"You earned "
            f"{format_currency(total_income)} "
            f"but spent "
            f"{format_currency(total_expenses)}. "
            f"Your expenses currently exceed your income."
        )

    # -----------------------------------------------------
    # RECENT ACTIVITY
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Recent Activity'
        '</div>',
        unsafe_allow_html=True
    )

    recent_income = [

        {
            "Date": item.get("date"),
            "Type": "Income",
            "Category": item.get(
                "source",
                "Income"
            ),
            "Amount": item.get(
                "amount",
                0
            )
        }

        for item in current_incomes
    ]

    recent_expenses = [

        {
            "Date": item.get("date"),
            "Type": "Expense",
            "Category": item.get(
                "category",
                "Expense"
            ),
            "Amount": item.get(
                "amount",
                0
            )
        }

        for item in current_expenses
    ]

    activity = (
        recent_income +
        recent_expenses
    )

    if activity:

        activity_df = pd.DataFrame(
            activity
        )

        activity_df = (
            activity_df
            .sort_values(
                "Date",
                ascending=False
            )
            .head(5)
        )

        st.dataframe(
            activity_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No transactions recorded for this period."
        )


# =========================================================
# ADD TRANSACTION
# =========================================================

elif page == "Add Transaction":

    st.markdown(
        '<div class="main-title">'
        'Add Transaction'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Record income and expenses to keep your '
        'financial dashboard accurate.'
        '</div>',
        unsafe_allow_html=True
    )

    transaction_type = st.radio(
        "Transaction Type",
        [
            "Income",
            "Expense"
        ],
        horizontal=True
    )

    st.markdown(
        "### Transaction Details"
    )

    if transaction_type == "Income":

        source = st.selectbox(
            "Income Source",
            [
                "Salary",
                "Freelance",
                "Business",
                "Bonus",
                "Interest",
                "Other"
            ]
        )

    else:

        category = st.selectbox(
            "Expense Category",
            [
                "Rent",
                "Food",
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
        "Amount (₹)",
        min_value=0.0,
        step=100.0
    )

    transaction_date = st.date_input(
        "Date",
        value=date.today()
    )

    if st.button(
        "Save Transaction",
        use_container_width=True
    ):

        if amount <= 0:

            st.error(
                "Please enter an amount greater than zero."
            )

        else:

            transaction_date_str = (
                transaction_date.strftime(
                    "%Y-%m-%d"
                )
            )

            if transaction_type == "Income":

                save_income(
                    source,
                    amount,
                    transaction_date_str
                )

                st.success(
                    "Income added successfully."
                )

            else:

                save_expense(
                    category,
                    amount,
                    transaction_date_str
                )

                st.success(
                    "Expense added successfully."
                )

            st.rerun()


# =========================================================
# HISTORY
# =========================================================

elif page == "History":

    st.markdown(
        '<div class="main-title">'
        'Transaction History'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Review your financial activity and monthly performance.'
        '</div>',
        unsafe_allow_html=True
    )

    history = get_monthly_history()

    if history:

        history_df = pd.DataFrame(
            history
        )

        st.markdown(
            "### Monthly Summary"
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        if len(history_df) > 0:

            fig = go.Figure()

            if "income" in history_df.columns:

                fig.add_trace(
                    go.Scatter(
                        x=history_df["month"],
                        y=history_df["income"],
                        mode="lines+markers",
                        name="Income"
                    )
                )

            if "expenses" in history_df.columns:

                fig.add_trace(
                    go.Scatter(
                        x=history_df["month"],
                        y=history_df["expenses"],
                        mode="lines+markers",
                        name="Expenses"
                    )
                )

            fig.update_layout(
                title="Monthly Performance",

                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",

                font=dict(
                    color="#dbe5f2"
                ),

                yaxis=dict(
                    gridcolor="#202d43",
                    zeroline=False
                ),

                margin=dict(
                    l=20,
                    r=20,
                    t=55,
                    b=20
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

    else:

        st.info(
            "No monthly history available yet."
        )

    st.markdown(
        "### Transaction History"
    )

    all_income = load_income()

    all_expenses = load_expenses()

    transaction_rows = []

    for item in all_income:

        transaction_rows.append(
            {
                "ID": item.get("id"),
                "Date": item.get("date"),
                "Type": "Income",
                "Category": item.get(
                    "source",
                    "Income"
                ),
                "Amount": item.get(
                    "amount",
                    0
                )
            }
        )

    for item in all_expenses:

        transaction_rows.append(
            {
                "ID": item.get("id"),
                "Date": item.get("date"),
                "Type": "Expense",
                "Category": item.get(
                    "category",
                    "Expense"
                ),
                "Amount": item.get(
                    "amount",
                    0
                )
            }
        )

    if transaction_rows:

        transaction_df = pd.DataFrame(
            transaction_rows
        )

        transaction_df = (
            transaction_df
            .sort_values(
                "Date",
                ascending=False
            )
        )

        st.dataframe(
            transaction_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No transactions recorded."
        )

    st.markdown(
        "### Delete Transaction"
    )

    delete_type = st.radio(
        "Select transaction type",
        [
            "Income",
            "Expense"
        ],
        horizontal=True
    )

    if delete_type == "Income":

        deletable = all_income

    else:

        deletable = all_expenses

    if deletable:

        options = {}

        for item in deletable:

            item_id = item.get("id")

            if delete_type == "Income":

                label = (
                    f"#{item_id} | "
                    f"{item.get('source')} | "
                    f"₹{item.get('amount'):,.2f}"
                )

            else:

                label = (
                    f"#{item_id} | "
                    f"{item.get('category')} | "
                    f"₹{item.get('amount'):,.2f}"
                )

            options[label] = item_id

        selected_transaction = st.selectbox(
            "Choose transaction",
            list(options.keys())
        )

        if st.button(
            "Delete Transaction"
        ):

            selected_id = options[
                selected_transaction
            ]

            if delete_type == "Income":

                delete_income(
                    selected_id
                )

            else:

                delete_expense(
                    selected_id
                )

            st.success(
                "Transaction deleted successfully."
            )

            st.rerun()

    else:

        st.info(
            "No transactions available to delete."
        )


# =========================================================
# SPENDING ANALYSIS
# =========================================================

elif page == "Spending Analysis":

    st.markdown(
        '<div class="main-title">'
        'Spending Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Understand where your money is going and '
        'identify your largest spending areas.'
        '</div>',
        unsafe_allow_html=True
    )

    month_options = (
        ["All Time"] +
        available_months
    )

    selected_month = st.selectbox(
        "Analysis Period",
        month_options,
        format_func=month_display
    )

    selected_expenses = filter_by_month(
        expenses,
        selected_month
    )

    category_totals = (
        calculate_category_totals(
            selected_expenses
        )
    )

    total_spending = sum(
        category_totals.values()
    )

    highest_category, highest_amount = (
        find_highest_spending_category(
            selected_expenses
        )
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Total Spending",
            format_currency(
                total_spending
            )
        )

    with c2:

        st.metric(
            "Categories",
            len(category_totals)
        )

    with c3:

        st.metric(
            "Top Category",
            highest_category
            if highest_category
            else "None"
        )

    if category_totals:

        left, right = st.columns(2)

        with left:

            data = pd.DataFrame(
                {
                    "Category":
                        list(
                            category_totals.keys()
                        ),

                    "Amount":
                        list(
                            category_totals.values()
                        )
                }
            )

            fig = px.bar(
                data,
                x="Category",
                y="Amount",
                text="Amount"
            )

            fig.update_traces(
                texttemplate="₹%{text:,.0f}",
                textposition="outside"
            )

            fig.update_layout(
                title="Spending by Category",

                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",

                font=dict(
                    color="#dbe5f2"
                ),

                yaxis=dict(
                    gridcolor="#202d43",
                    zeroline=False
                ),

                margin=dict(
                    l=20,
                    r=20,
                    t=55,
                    b=20
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        with right:

            pie_fig = create_spending_chart(
                selected_expenses
            )

            if pie_fig:

                st.plotly_chart(
                    pie_fig,
                    use_container_width=True,
                    config={
                        "displayModeBar": False
                    }
                )

        if highest_category:

            percentage = (
                highest_amount /
                total_spending *
                100
            )

            st.markdown(
                f"""
                <div class="insight-card">

                    <div class="insight-title">
                        💡 Spending Insight
                    </div>

                    <div class="insight-text">

                        <b>{highest_category}</b>
                        is your highest spending category
                        with
                        <b>
                            {format_currency(highest_amount)}
                        </b>,

                        representing
                        <b>
                            {percentage:.1f}%
                        </b>

                        of your total spending.

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No expenses recorded for this period."
        )


# =========================================================
# BUDGET PLANNER
# =========================================================

elif page == "Budget Planner":

    st.markdown(
        '<div class="main-title">'
        'Budget Planner'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Set monthly spending limits and compare your budget '
        'with your actual expenses.'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # MONTH SELECTION
    # -----------------------------------------------------

    current_month = date.today().strftime(
        "%Y-%m"
    )

    budget_month_options = list(
        available_months
    )

    if current_month not in budget_month_options:

        budget_month_options.insert(
            0,
            current_month
        )

    if not budget_month_options:

        budget_month_options = [
            current_month
        ]

    selected_budget_month = st.selectbox(
        "Budget Month",
        budget_month_options,
        format_func=month_display
    )

    # -----------------------------------------------------
    # ADD BUDGET
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Create Monthly Budget'
        '</div>',
        unsafe_allow_html=True
    )

    budget_col1, budget_col2, budget_col3 = st.columns(
        [1.3, 1, 0.8]
    )

    with budget_col1:

        budget_category = st.selectbox(
            "Expense Category",
            [
                "Rent",
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Entertainment",
                "Healthcare",
                "Education",
                "Other"
            ]
        )

    with budget_col2:

        budget_amount = st.number_input(
            "Budget Amount (₹)",
            min_value=0.0,
            step=500.0,
            value=5000.0
        )

    with budget_col3:

        st.write("")
        st.write("")

        add_budget_button = st.button(
            "Add Budget",
            use_container_width=True
        )

    if add_budget_button:

        if budget_amount <= 0:

            st.error(
                "Please enter a budget amount greater than zero."
            )

        else:

            save_budget(
                budget_category,
                budget_amount,
                selected_budget_month
            )

            st.success(
                f"{budget_category} budget added successfully."
            )

            st.rerun()

    # -----------------------------------------------------
    # LOAD BUDGETS
    # -----------------------------------------------------

    budget_rows = get_budgets(
        selected_budget_month
    )

    category_budgets = {}

    for row in budget_rows:

        if isinstance(row, (tuple, list)):

            if len(row) >= 4:

                budget_id = row[0]
                category = row[1]
                amount = float(row[2])
                month = row[3]

                category_budgets[category] = amount

    # -----------------------------------------------------
    # ACTUAL SPENDING
    # -----------------------------------------------------

    month_expenses = filter_by_month(
        expenses,
        selected_budget_month
    )

    category_totals = calculate_category_totals(
        month_expenses
    )

    # -----------------------------------------------------
    # BUDGET OVERVIEW
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Budget Overview'
        '</div>',
        unsafe_allow_html=True
    )

    if category_budgets:

        total_budget = calculate_total_budget(
            category_budgets
        )

        total_spending = calculate_total_spending(
            category_totals
        )

        remaining_budget = calculate_remaining_budget(
            total_budget,
            total_spending
        )

        overview_col1, overview_col2, overview_col3 = (
            st.columns(3)
        )

        with overview_col1:

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        TOTAL BUDGET
                    </div>

                    <div class="metric-value metric-blue">
                        {format_currency(total_budget)}
                    </div>

                    <div class="metric-subtitle">
                        Planned monthly spending
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with overview_col2:

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        ACTUAL SPENDING
                    </div>

                    <div class="metric-value metric-negative">
                        {format_currency(total_spending)}
                    </div>

                    <div class="metric-subtitle">
                        Recorded expenses
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with overview_col3:

            remaining_class = (
                "metric-positive"
                if remaining_budget >= 0
                else "metric-negative"
            )

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        REMAINING BUDGET
                    </div>

                    <div class="metric-value {remaining_class}">
                        {format_currency(remaining_budget)}
                    </div>

                    <div class="metric-subtitle">
                        Budget minus spending
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        # -------------------------------------------------
        # CATEGORY STATUS
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Category Budget Status'
            '</div>',
            unsafe_allow_html=True
        )

        budget_status = calculate_budget_status(
            category_budgets,
            category_totals
        )

        for category, status_data in budget_status.items():

            budget = status_data["budget"]
            spent = status_data["spent"]
            remaining = status_data["remaining"]
            percentage_used = status_data["percentage_used"]
            status = status_data["status"]

            st.markdown(
                f"""
                <div class="budget-card">

                    <div class="budget-category">
                        {category}
                    </div>

                    <div class="budget-details">
                        Spent {format_currency(spent)}
                        of
                        {format_currency(budget)}
                        &nbsp;·&nbsp;
                        {percentage_used:.1f}% used
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            progress_value = min(
                percentage_used / 100,
                1.0
            )

            st.progress(
                progress_value
            )

            if status == "Over Budget":

                st.error(
                    f"{category}: Over budget by "
                    f"{format_currency(abs(remaining))}."
                )

            elif status == "Almost Reached":

                st.warning(
                    f"{category}: Almost reached the budget. "
                    f"{format_currency(max(remaining, 0))} remaining."
                )

            else:

                st.success(
                    f"{category}: Within budget. "
                    f"{format_currency(max(remaining, 0))} remaining."
                )

        # -------------------------------------------------
        # BUDGET VS ACTUAL CHART
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Budget vs Actual Spending'
            '</div>',
            unsafe_allow_html=True
        )

        budget_fig = create_budget_snapshot_chart(
            category_budgets,
            category_totals
        )

        if budget_fig:

            st.plotly_chart(
                budget_fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        # -------------------------------------------------
        # DELETE BUDGET
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Manage Budgets'
            '</div>',
            unsafe_allow_html=True
        )

        if budget_rows:

            budget_options = {}

            for row in budget_rows:

                if len(row) >= 4:

                    budget_id = row[0]
                    category = row[1]
                    amount = float(row[2])

                    label = (
                        f"#{budget_id} | "
                        f"{category} | "
                        f"{format_currency(amount)}"
                    )

                    budget_options[label] = budget_id

            if budget_options:

                selected_budget = st.selectbox(
                    "Choose budget to delete",
                    list(
                        budget_options.keys()
                    )
                )

                if st.button(
                    "Delete Budget"
                ):

                    selected_budget_id = budget_options[
                        selected_budget
                    ]

                    delete_budget(
                        selected_budget_id
                    )

                    st.success(
                        "Budget deleted successfully."
                    )

                    st.rerun()

    else:

        st.info(
            f"No budgets created for "
            f"{month_display(selected_budget_month)} yet. "
            "Create a category budget above to start planning your spending."
        )


# =========================================================
# CALCULATORS
# =========================================================

elif page == "Calculators":

    st.markdown(
        '<div class="main-title">'
        'Financial Calculators'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Explore common financial calculations using '
        'simple interactive tools.'
        '</div>',
        unsafe_allow_html=True
    )

    calculator = st.selectbox(
        "Choose Calculator",
        [
            "Simple Interest",
            "Compound Interest",
            "SIP",
            "EMI"
        ]
    )

    if calculator == "Simple Interest":

        st.subheader(
            "Simple Interest Calculator"
        )

        principal = st.number_input(
            "Principal (₹)",
            min_value=0.0,
            value=10000.0
        )

        rate = st.number_input(
            "Annual Interest Rate (%)",
            min_value=0.0,
            value=5.0
        )

        time = st.number_input(
            "Time (Years)",
            min_value=0.0,
            value=2.0
        )

        if st.button(
            "Calculate Simple Interest"
        ):

            interest, amount = (
                calculate_simple_interest(
                    principal,
                    rate,
                    time
                )
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Interest",
                    format_currency(
                        interest
                    )
                )

            with col2:

                st.metric(
                    "Final Amount",
                    format_currency(
                        amount
                    )
                )

    elif calculator == "Compound Interest":

        st.subheader(
            "Compound Interest Calculator"
        )

        principal = st.number_input(
            "Principal (₹)",
            min_value=0.0,
            value=10000.0
        )

        rate = st.number_input(
            "Annual Interest Rate (%)",
            min_value=0.0,
            value=7.0
        )

        time = st.number_input(
            "Time (Years)",
            min_value=0.0,
            value=5.0
        )

        compounds = st.number_input(
            "Compounds Per Year",
            min_value=1,
            value=12
        )

        if st.button(
            "Calculate Compound Interest"
        ):

            interest, amount = (
                calculate_compound_interest(
                    principal,
                    rate,
                    time,
                    compounds
                )
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Interest",
                    format_currency(
                        interest
                    )
                )

            with col2:

                st.metric(
                    "Final Amount",
                    format_currency(
                        amount
                    )
                )

    elif calculator == "SIP":

        st.subheader(
            "SIP Calculator"
        )

        monthly_investment = st.number_input(
            "Monthly Investment (₹)",
            min_value=0.0,
            value=5000.0
        )

        annual_rate = st.number_input(
            "Expected Annual Return (%)",
            min_value=0.0,
            value=12.0
        )

        years = st.number_input(
            "Investment Period (Years)",
            min_value=1,
            value=10
        )

        if st.button(
            "Calculate SIP"
        ):

            invested, returns, final_value = (
                calculate_sip(
                    monthly_investment,
                    annual_rate,
                    years
                )
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Total Invested",
                    format_currency(
                        invested
                    )
                )

            with c2:

                st.metric(
                    "Estimated Returns",
                    format_currency(
                        returns
                    )
                )

            with c3:

                st.metric(
                    "Final Value",
                    format_currency(
                        final_value
                    )
                )

    else:

        st.subheader(
            "EMI Calculator"
        )

        principal = st.number_input(
            "Loan Amount (₹)",
            min_value=0.0,
            value=500000.0
        )

        annual_rate = st.number_input(
            "Annual Interest Rate (%)",
            min_value=0.0,
            value=8.5
        )

        years = st.number_input(
            "Loan Tenure (Years)",
            min_value=1,
            value=5
        )

        if st.button(
            "Calculate EMI"
        ):

            emi, total_interest, total_payment = (
                calculate_emi(
                    principal,
                    annual_rate,
                    years
                )
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Monthly EMI",
                    format_currency(
                        emi
                    )
                )

            with c2:

                st.metric(
                    "Total Interest",
                    format_currency(
                        total_interest
                    )
                )

            with c3:

                st.metric(
                    "Total Payment",
                    format_currency(
                        total_payment
                    )
                )


# =========================================================
# AI FINANCIAL ADVISOR
# =========================================================

elif page == "AI Financial Advisor":

    st.markdown(
        '<div class="main-title">'
        'AI Financial Advisor'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Use AI to turn your financial data into '
        'simple, practical observations.'
        '</div>',
        unsafe_allow_html=True
    )

    total_income, total_expenses, balance, savings_rate = (
        calculate_totals(
            incomes,
            expenses
        )
    )

    expense_ratio = (
        total_expenses /
        total_income *
        100
        if total_income > 0
        else 0
    )

    highest_category, highest_amount = (
        find_highest_spending_category(
            expenses
        )
    )

    health_score, health_label = (
        calculate_financial_health_score(
            total_income,
            total_expenses,
            savings_rate
        )
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Income",
            format_currency(
                total_income
            )
        )

    with c2:

        st.metric(
            "Expenses",
            format_currency(
                total_expenses
            )
        )

    with c3:

        st.metric(
            "Balance",
            format_currency(
                balance
            )
        )

    with c4:

        st.metric(
            "Savings Rate",
            f"{savings_rate:.1f}%"
        )

    st.markdown(
        '<div class="section-title">'
        'Financial Snapshot'
        '</div>',
        unsafe_allow_html=True
    )

    snapshot_col1, snapshot_col2 = st.columns(2)

    with snapshot_col1:

        if highest_category:

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        HIGHEST SPENDING CATEGORY
                    </div>

                    <div class="metric-value">
                        {highest_category}
                    </div>

                    <div class="metric-subtitle">
                        {format_currency(highest_amount)}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.info(
                "No spending category available yet."
            )

    with snapshot_col2:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    FINANCIAL HEALTH
                </div>

                <div class="metric-value metric-positive">
                    {health_score}/100
                </div>

                <div class="metric-subtitle">
                    {health_label}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.info(
        "The AI advisor provides general financial "
        "guidance based on the information recorded "
        "in your app. It does not provide guaranteed "
        "or professional investment advice."
    )

    if st.button(
        "✨ Generate AI Financial Analysis",
        use_container_width=True
    ):

        prompt = create_financial_prompt(
            total_income=total_income,
            total_expenses=total_expenses,
            remaining_balance=balance,
            savings_percentage=savings_rate,
            highest_category=highest_category,
            highest_amount=highest_amount
        )

        with st.spinner(
            "Analyzing your financial information..."
        ):

            try:

                advice = get_ai_financial_advice(
                    prompt
                )

                st.markdown(
                    "### 🤖 AI Analysis"
                )

                st.markdown(
                    '<div class="insight-card">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    advice
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            except Exception as error:

                st.error(
                    "The AI service is currently unavailable. "
                    "Please try again later."
                )

                st.caption(
                    f"Technical information: {error}"
                )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#52627a;
        font-size:0.76rem;
        margin-top:55px;
        padding-top:22px;
        border-top:1px solid #1b273b;
        letter-spacing:0.2px;
    ">
        AI Finance Assistant
        &nbsp;·&nbsp;
        Python
        &nbsp;·&nbsp;
        Streamlit
        &nbsp;·&nbsp;
        SQLite
        &nbsp;·&nbsp;
        AI
    </div>
    """,
    unsafe_allow_html=True
)