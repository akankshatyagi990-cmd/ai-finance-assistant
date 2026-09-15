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
                circle at 10% 0%,
                rgba(99, 102, 241, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(16, 185, 129, 0.08),
                transparent 28%
            ),
            #0b1020;

        color: #f8fafc;
    }

    section[data-testid="stSidebar"] {
        background: #0f172a;
        border-right: 1px solid #1e293b;
    }

    section[data-testid="stSidebar"] * {
        color: #e2e8f0;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    .welcome-card {
        background:
            linear-gradient(
                135deg,
                rgba(30, 41, 59, 0.96),
                rgba(15, 23, 42, 0.96)
            );

        border: 1px solid #263449;
        border-radius: 22px;
        padding: 26px 30px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }

    .welcome-card:after {
        content: "";
        position: absolute;
        width: 180px;
        height: 180px;
        border-radius: 50%;
        right: -60px;
        top: -70px;
        background: rgba(99, 102, 241, 0.16);
    }

    .welcome-title {
        font-size: 1.55rem;
        font-weight: 750;
        margin-bottom: 5px;
    }

    .welcome-text {
        color: #94a3b8;
        font-size: 0.95rem;
    }

    .metric-card {
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid #263449;
        border-radius: 18px;
        padding: 20px;
        min-height: 125px;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 0.82rem;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 1.55rem;
        font-weight: 750;
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

    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    .insight-card {
        background: rgba(30, 41, 59, 0.72);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 16px 18px;
        margin-bottom: 10px;
    }

    .insight-title {
        font-weight: 700;
        margin-bottom: 5px;
    }

    .insight-text {
        color: #cbd5e1;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    .alert-card {
        background: rgba(127, 29, 29, 0.18);
        border: 1px solid rgba(248, 113, 113, 0.35);
        border-radius: 16px;
        padding: 16px 18px;
        margin-bottom: 10px;
    }

    .trend-card {
        background: #111827;
        border: 1px solid #263449;
        border-radius: 16px;
        padding: 18px;
    }

    .trend-label {
        color: #94a3b8;
        font-size: 0.8rem;
    }

    .trend-value {
        font-size: 1.25rem;
        font-weight: 700;
        margin-top: 5px;
    }

    .health-card {
        background:
            linear-gradient(
                135deg,
                rgba(16, 185, 129, 0.10),
                rgba(15, 23, 42, 0.90)
            );

        border: 1px solid rgba(52, 211, 153, 0.25);
        border-radius: 18px;
        padding: 20px;
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
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
# IMPORTANT:
# SQLite currently returns tuples.
# The rest of the application uses dictionaries.
# These functions convert tuples -> dictionaries.
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

    return (
        total_income,
        total_expenses,
        balance,
        savings_rate
    )


def calculate_health_score(
    savings_rate,
    expense_ratio
):

    score = 50

    if savings_rate >= 40:

        score += 30

    elif savings_rate >= 30:

        score += 20

    elif savings_rate >= 20:

        score += 10

    elif savings_rate < 0:

        score -= 30


    if expense_ratio <= 50:

        score += 20

    elif expense_ratio <= 70:

        score += 10

    elif expense_ratio > 90:

        score -= 20


    return max(
        0,
        min(100, score)
    )


def get_health_label(score):

    if score >= 80:

        return "Excellent"

    elif score >= 65:

        return "Healthy"

    elif score >= 50:

        return "Moderate"

    elif score >= 30:

        return "Needs Attention"

    else:

        return "Critical"


def format_currency(value):

    return f"₹{value:,.2f}"


def filter_by_month(
    records,
    selected_month
):

    if selected_month == "All Time":

        return records


    filtered = []

    for record in records:

        record_date = record.get(
            "date"
        )

        if record_date:

            if str(record_date)[:7] == selected_month:

                filtered.append(record)


    return filtered


def get_available_months(
    incomes,
    expenses
):

    months = set()


    for record in incomes + expenses:

        record_date = record.get(
            "date"
        )

        if record_date:

            months.add(
                str(record_date)[:7]
            )


    return sorted(
        months,
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


def get_previous_month(
    selected_month
):

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
        title="Money Movement",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#e2e8f0"
        ),

        yaxis=dict(
            gridcolor="#263449"
        ),

        xaxis=dict(
            title=""
        ),

        margin=dict(
            l=20,
            r=20,
            t=55,
            b=20
        )
    )


    return fig


def create_spending_chart(
    expenses
):

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
        hole=0.55
    )


    fig.update_layout(
        title="Spending Breakdown",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#e2e8f0"
        ),

        margin=dict(
            l=10,
            r=10,
            t=55,
            b=10
        ),

        legend=dict(
            orientation="h"
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


            monthly_data[month][
                "Income"
            ] += income["amount"]


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


            monthly_data[month][
                "Expenses"
            ] += expense["amount"]


    if not monthly_data:

        return None


    rows = []


    for month in sorted(
        monthly_data
    ):

        rows.append(
            {
                "Month": month,

                "Income":
                    monthly_data[month][
                        "Income"
                    ],

                "Expenses":
                    monthly_data[month][
                        "Expenses"
                    ]
            }
        )


    data = pd.DataFrame(
        rows
    )


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
            color="#e2e8f0"
        ),

        yaxis=dict(
            gridcolor="#263449"
        ),

        margin=dict(
            l=20,
            r=20,
            t=55,
            b=20
        )
    )


    return fig


# =========================================================
# LOAD APPLICATION DATA
# =========================================================

incomes = load_income()

expenses = load_expenses()


available_months = (
    get_available_months(
        incomes,
        expenses
    )
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <div style="
        font-size:1.45rem;
        font-weight:800;
        margin-bottom:5px;
    ">
        💼 AI Finance
    </div>

    <div style="
        color:#94a3b8;
        font-size:0.85rem;
        margin-bottom:20px;
    ">
        Personal Financial Intelligence
    </div>
    """,
    unsafe_allow_html=True
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
    ]
)


st.sidebar.markdown("---")


st.sidebar.caption(
    "AI Finance Assistant"
)


st.sidebar.caption(
    "Finance + Python + AI"
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
        'Your personal financial cockpit — '
        'understand your money at a glance.'
        '</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # MONTH SELECTOR
    # -----------------------------------------------------

    month_options = (
        ["All Time"] +
        available_months
    )


    selected_month = st.selectbox(
        "View financial data for",
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


    # -----------------------------------------------------
    # WELCOME
    # -----------------------------------------------------

    if balance > 0:

        message = (
            "You're currently spending less than "
            "you earn. Keep building that financial momentum."
        )

    elif balance == 0:

        message = (
            "Your income and expenses are currently balanced."
        )

    else:

        message = (
            "Your expenses are higher than your income. "
            "Let's identify where your money is going."
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


    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    TOTAL INCOME
                </div>

                <div class="
                    metric-value
                    metric-positive
                ">
                    {format_currency(total_income)}
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

                <div class="
                    metric-value
                    metric-negative
                ">
                    {format_currency(total_expenses)}
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

                <div class="
                    metric-value
                    {balance_class}
                ">
                    {format_currency(balance)}
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

                <div class="
                    metric-value
                    metric-purple
                ">
                    {savings_rate:.1f}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # FINANCIAL HEALTH
    # -----------------------------------------------------

    health_score = calculate_health_score(
        savings_rate,
        expense_ratio
    )


    health_label = get_health_label(
        health_score
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
                    color:#94a3b8;
                    font-size:0.8rem;
                ">
                    FINANCIAL HEALTH SCORE
                </div>

                <div style="
                    font-size:2.3rem;
                    font-weight:800;
                    margin:5px 0;
                ">
                    {health_score}/100
                </div>

                <div style="
                    color:#34d399;
                    font-weight:700;
                ">
                    {health_label}
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
            "Your score considers savings rate "
            "and spending level."
        )


        if savings_rate >= 30:

            st.success(
                "Strong savings performance. "
                "Keep maintaining this habit."
            )

        elif savings_rate >= 0:

            st.info(
                "Your finances are positive, "
                "but there is room to improve your savings rate."
            )

        else:

            st.error(
                "Your current expenses are higher "
                "than your income."
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


        # -------------------------------------------------
        # TREND CARDS
        # -------------------------------------------------

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
                        {symbol}
                        {abs(income_change):.1f}%
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
                        {symbol}
                        {abs(expense_change):.1f}%
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
                        {symbol}
                        {abs(savings_change):.1f}%
                    </div>

                    <div class="trend-label">
                        vs previous month
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        # -------------------------------------------------
        # ALERTS
        # -------------------------------------------------

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


        # -------------------------------------------------
        # INSIGHTS
        # -------------------------------------------------

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
            "Select a specific month to compare it "
            "with the previous month and unlock "
            "Financial Intelligence."
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
            use_container_width=True
        )


    with chart_col2:

        spending_fig = create_spending_chart(
            current_expenses
        )


        if spending_fig:

            st.plotly_chart(
                spending_fig,
                use_container_width=True
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
            use_container_width=True
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
        'Keep your financial records accurate '
        'and up to date.'
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


    description = st.text_input(
        "Description (optional)"
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
        'Review your financial activity '
        'and monthly performance.'
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
                    color="#e2e8f0"
                ),

                yaxis=dict(
                    gridcolor="#263449"
                )
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


    else:

        st.info(
            "No monthly history available yet."
        )


    # -----------------------------------------------------
    # TRANSACTION HISTORY
    # -----------------------------------------------------

    st.markdown(
        "### Transaction History"
    )


    # IMPORTANT:
    # Use load_income/load_expenses instead of directly
    # using database tuples.

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


    # -----------------------------------------------------
    # DELETE TRANSACTION
    # -----------------------------------------------------

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
        'Understand where your money is going.'
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
                    color="#e2e8f0"
                ),

                yaxis=dict(
                    gridcolor="#263449"
                )
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


        with right:

            pie_fig = create_spending_chart(
                selected_expenses
            )


            if pie_fig:

                st.plotly_chart(
                    pie_fig,
                    use_container_width=True
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
        'Explore common financial calculations.'
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


    # -----------------------------------------------------
    # SIMPLE INTEREST
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # COMPOUND INTEREST
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # SIP
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # EMI
    # -----------------------------------------------------

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
        'Get personalized financial observations '
        'using your transaction data.'
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
        "### Financial Snapshot"
    )


    if highest_category:

        st.write(
            f"**Highest spending category:** "
            f"{highest_category}"
        )


        st.write(
            f"**Amount:** "
            f"{format_currency(highest_amount)}"
        )

    else:

        st.write(
            "No spending category available yet."
        )


    st.write(
        f"**Expense ratio:** "
        f"{expense_ratio:.1f}%"
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
                    f"""
                    <div class="insight-card">

                        <div class="insight-text"
                             style="font-size:1rem;">

                            {advice}

                        </div>

                    </div>
                    """,
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
        color:#64748b;
        font-size:0.8rem;
        margin-top:45px;
        padding-top:20px;
        border-top:1px solid #1e293b;
    ">
        AI Finance Assistant ·
        Built with Python, Streamlit & AI
    </div>
    """,
    unsafe_allow_html=True
)