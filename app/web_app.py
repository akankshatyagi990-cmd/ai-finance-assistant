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
# PROFESSIONAL + COLORFUL STYLING
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       MAIN APP
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 85% 5%,
                rgba(78, 91, 220, 0.10),
                transparent 25%
            ),
            radial-gradient(
                circle at 10% 20%,
                rgba(40, 180, 130, 0.07),
                transparent 22%
            ),
            #0a0e14;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #10151d 0%,
                #0d1219 100%
            );
        border-right: 1px solid #252d38;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
        padding-left: 1.3rem;
        padding-right: 1.3rem;
    }

    .sidebar-brand {
        font-size: 1.2rem;
        font-weight: 750;
        color: #f4f7fa;
        letter-spacing: -0.4px;
    }

    .sidebar-subtitle {
        font-size: 0.78rem;
        color: #8793a2;
        line-height: 1.55;
        margin-top: 0.35rem;
        margin-bottom: 2rem;
    }


    /* =====================================================
       TYPOGRAPHY
       ===================================================== */

    h1 {
        font-size: 2.45rem !important;
        font-weight: 750 !important;
        letter-spacing: -1.2px !important;
        color: #f5f7fa !important;
    }

    h2 {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #f0f3f6 !important;
    }

    h3 {
        font-size: 1.05rem !important;
        font-weight: 650 !important;
        color: #e7ebef !important;
    }

    p {
        color: #9ca7b5;
    }


    /* =====================================================
       PAGE HEADER
       ===================================================== */

    .page-eyebrow {
        color: #8290a1;
        font-size: 0.74rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.4rem;
    }

    .page-description {
        color: #8f9aa8;
        font-size: 0.92rem;
        margin-top: -0.75rem;
        margin-bottom: 1.8rem;
    }


    /* =====================================================
       DASHBOARD WELCOME BANNER
       ===================================================== */

    .welcome-banner {
        position: relative;
        overflow: hidden;
        background:
            linear-gradient(
                135deg,
                rgba(52, 65, 170, 0.30),
                rgba(21, 105, 91, 0.18)
            );
        border: 1px solid rgba(108, 122, 230, 0.25);
        border-radius: 18px;
        padding: 1.45rem 1.6rem;
        margin-bottom: 1.25rem;
    }

    .welcome-banner:after {
        content: "";
        position: absolute;
        width: 180px;
        height: 180px;
        right: -60px;
        top: -90px;
        border-radius: 50%;
        background: rgba(117, 101, 255, 0.12);
    }

    .welcome-title {
        color: #f4f7fa;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .welcome-text {
        color: #aab4c1;
        font-size: 0.84rem;
    }


    /* =====================================================
       KPI CARDS
       ===================================================== */

    .metric-card {
        position: relative;
        overflow: hidden;
        background: rgba(18, 24, 32, 0.92);
        border: 1px solid #28313d;
        border-radius: 15px;
        padding: 1.25rem 1.3rem;
        min-height: 138px;
        transition: all 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        border-color: #3a4655;
    }

    .metric-card:after {
        content: "";
        position: absolute;
        right: -30px;
        bottom: -50px;
        width: 120px;
        height: 120px;
        border-radius: 50%;
        opacity: 0.13;
    }

    .metric-income:after {
        background: #42d392;
    }

    .metric-expense:after {
        background: #ff7373;
    }

    .metric-balance:after {
        background: #5b8cff;
    }

    .metric-saving:after {
        background: #a97cff;
    }

    .metric-icon {
        font-size: 1.05rem;
        margin-bottom: 0.55rem;
    }

    .metric-label {
        color: #8793a1;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.75px;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        color: #f4f6f8;
        font-size: 1.62rem;
        font-weight: 750;
        letter-spacing: -0.7px;
    }

    .metric-small {
        color: #758191;
        font-size: 0.73rem;
        margin-top: 0.42rem;
    }


    /* =====================================================
       CONTENT CARDS
       ===================================================== */

    .content-card {
        background: rgba(18, 24, 32, 0.94);
        border: 1px solid #252e39;
        border-radius: 15px;
        padding: 1.35rem;
        margin-bottom: 1rem;
    }

    .card-title {
        color: #eef1f4;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .card-subtitle {
        color: #7f8b98;
        font-size: 0.77rem;
        margin-bottom: 1rem;
    }


    /* =====================================================
       HEALTH SCORE
       ===================================================== */

    .health-card {
        background:
            linear-gradient(
                145deg,
                rgba(28, 40, 53, 0.98),
                rgba(18, 25, 34, 0.98)
            );
        border: 1px solid #2b3744;
        border-radius: 15px;
        padding: 1.4rem;
        height: 100%;
    }

    .health-score {
        font-size: 3.2rem;
        font-weight: 800;
        color: #f4f6f8;
        line-height: 1;
    }

    .health-label {
        color: #8b97a5;
        font-size: 0.8rem;
        margin-top: 0.45rem;
        margin-bottom: 0.9rem;
    }

    .health-tip {
        color: #aab4c0;
        font-size: 0.78rem;
        line-height: 1.5;
        margin-top: 0.8rem;
    }


    /* =====================================================
       INSIGHTS
       ===================================================== */

    .insight-card {
        background:
            linear-gradient(
                135deg,
                rgba(53, 48, 100, 0.35),
                rgba(20, 28, 39, 0.96)
            );
        border: 1px solid rgba(116, 101, 219, 0.28);
        border-radius: 15px;
        padding: 1.35rem;
        height: 100%;
    }

    .insight-label {
        color: #a99aff;
        font-size: 0.7rem;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 0.65rem;
    }

    .insight-text {
        color: #e9edf1;
        font-size: 0.92rem;
        line-height: 1.6;
    }


    /* =====================================================
       MONEY STORY
       ===================================================== */

    .story-card {
        background:
            linear-gradient(
                135deg,
                rgba(21, 74, 68, 0.26),
                rgba(18, 24, 32, 0.98)
            );
        border: 1px solid rgba(67, 190, 145, 0.20);
        border-radius: 15px;
        padding: 1.35rem;
    }

    .story-title {
        color: #eef7f2;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.7rem;
    }

    .story-text {
        color: #a9b8b2;
        font-size: 0.85rem;
        line-height: 1.65;
    }


    /* =====================================================
       SECTION LABEL
       ===================================================== */

    .section-label {
        color: #e9edf1;
        font-size: 1.03rem;
        font-weight: 700;
        margin-top: 1.15rem;
        margin-bottom: 0.7rem;
    }


    /* =====================================================
       TRANSACTIONS
       ===================================================== */

    .transaction-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(18, 24, 32, 0.94);
        border: 1px solid #242d38;
        border-radius: 11px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.5rem;
        transition: border-color 0.2s ease;
    }

    .transaction-row:hover {
        border-color: #3b4755;
    }

    .transaction-name {
        color: #e7ebef;
        font-weight: 650;
        font-size: 0.86rem;
    }

    .transaction-date {
        color: #727e8d;
        font-size: 0.7rem;
        margin-top: 0.2rem;
    }

    .transaction-income {
        color: #56d993;
        font-weight: 700;
    }

    .transaction-expense {
        color: #ff7c7c;
        font-weight: 700;
    }


    /* =====================================================
       QUICK ACTIONS
       ===================================================== */

    .quick-action {
        background: #121820;
        border: 1px solid #29333f;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }

    .quick-icon {
        font-size: 1.3rem;
        margin-bottom: 0.3rem;
    }

    .quick-title {
        color: #e8edf1;
        font-size: 0.82rem;
        font-weight: 650;
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        border-radius: 9px;
        font-weight: 650;
        min-height: 42px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
    }


    /* =====================================================
       DATAFRAME
       ===================================================== */

    [data-testid="stDataFrame"] {
        border: 1px solid #242d38;
        border-radius: 10px;
        overflow: hidden;
    }


    /* =====================================================
       DIVIDERS
       ===================================================== */

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


def filter_by_month(items, selected_month):

    if selected_month == "All Time":
        return items

    filtered_items = []

    for item in items:

        item_month = str(item["date"])[:7]

        if item_month == selected_month:

            filtered_items.append(item)

    return filtered_items


def get_available_months(incomes, expenses):

    months = set()

    for item in incomes:

        months.add(
            str(item["date"])[:7]
        )

    for item in expenses:

        months.add(
            str(item["date"])[:7]
        )

    return sorted(
        list(months),
        reverse=True
    )


def month_display(month_value):

    if month_value == "All Time":
        return "All Time"

    try:

        return pd.to_datetime(
            month_value + "-01"
        ).strftime("%B %Y")

    except Exception:

        return month_value


def create_financial_chart(
    selected_incomes,
    selected_expenses
):

    income_by_month = {}

    expense_by_month = {}

    for item in selected_incomes:

        month = str(item["date"])[:7]

        income_by_month[month] = (
            income_by_month.get(month, 0)
            + item["amount"]
        )

    for item in selected_expenses:

        month = str(item["date"])[:7]

        expense_by_month[month] = (
            expense_by_month.get(month, 0)
            + item["amount"]
        )

    months = sorted(
        set(
            list(income_by_month.keys())
            + list(expense_by_month.keys())
        )
    )

    if len(months) == 0:

        return None

    chart_rows = []

    for month in months:

        chart_rows.append(
            {
                "Month": month_display(month),
                "Income": income_by_month.get(
                    month,
                    0
                ),
                "Expenses": expense_by_month.get(
                    month,
                    0
                )
            }
        )

    chart_df = pd.DataFrame(
        chart_rows
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=chart_df["Month"],
            y=chart_df["Income"],
            name="Income",
            mode="lines+markers",
            line=dict(
                width=3
            ),
            marker=dict(
                size=8
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Income: ₹%{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=chart_df["Month"],
            y=chart_df["Expenses"],
            name="Expenses",
            mode="lines+markers",
            line=dict(
                width=3
            ),
            marker=dict(
                size=8
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Expenses: ₹%{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        height=350,
        margin=dict(
            l=10,
            r=10,
            t=15,
            b=10
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#9ca7b5"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode="x unified",
        xaxis=dict(
            showgrid=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.06)",
            tickprefix="₹"
        )
    )

    return fig


def create_spending_chart(expenses):

    category_totals = calculate_category_totals(
        expenses
    )

    if len(category_totals) == 0:

        return None

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

    spending_df = spending_df.sort_values(
        "Amount",
        ascending=False
    )

    fig = px.pie(
        spending_df,
        names="Category",
        values="Amount",
        hole=0.62
    )

    fig.update_traces(
        textposition="outside",
        textinfo="percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Spent: ₹%{value:,.0f}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        height=350,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#dce2e8"
        ),
        showlegend=True,
        legend=dict(
            orientation="v"
        )
    )

    return fig


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
        ◈ AI Finance Assistant
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
            Understand your money at a glance and discover where
            your financial habits are taking you.
        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # MONTH SELECTOR
    # =====================================================

    available_months = get_available_months(
        incomes,
        expenses
    )

    month_options = ["All Time"] + available_months

    selected_month = st.selectbox(
        "View financial period",
        month_options,
        format_func=month_display
    )

    selected_incomes = filter_by_month(
        incomes,
        selected_month
    )

    selected_expenses = filter_by_month(
        expenses,
        selected_month
    )

    (
        selected_income_total,
        selected_expense_total,
        selected_balance,
        selected_savings_rate
    ) = calculate_totals(
        selected_incomes,
        selected_expenses
    )

    selected_health_score = calculate_health_score(
        selected_savings_rate,
        selected_income_total,
        selected_expense_total
    )

    selected_health_label = get_health_label(
        selected_health_score
    )


    # =====================================================
    # WELCOME BANNER
    # =====================================================

    period_text = month_display(
        selected_month
    )

    st.markdown(
        f"""
        <div class="welcome-banner">

            <div class="welcome-title">
                Your financial cockpit
            </div>

            <div class="welcome-text">
                Here's how your finances look for
                <strong>{period_text}</strong>.
                Explore the charts to discover your money patterns.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # KPI CARDS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card metric-income">

                <div class="metric-icon">↗</div>

                <div class="metric-label">
                    Income
                </div>

                <div class="metric-value">
                    {format_currency(selected_income_total)}
                </div>

                <div class="metric-small">
                    Money coming in
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card metric-expense">

                <div class="metric-icon">↘</div>

                <div class="metric-label">
                    Expenses
                </div>

                <div class="metric-value">
                    {format_currency(selected_expense_total)}
                </div>

                <div class="metric-small">
                    Money going out
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        balance_label = (
            "Available to save"
            if selected_balance >= 0
            else "Overspent amount"
        )

        st.markdown(
            f"""
            <div class="metric-card metric-balance">

                <div class="metric-icon">◆</div>

                <div class="metric-label">
                    Balance
                </div>

                <div class="metric-value">
                    {format_currency(selected_balance)}
                </div>

                <div class="metric-small">
                    {balance_label}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""
            <div class="metric-card metric-saving">

                <div class="metric-icon">✦</div>

                <div class="metric-label">
                    Savings Rate
                </div>

                <div class="metric-value">
                    {selected_savings_rate:.1f}%
                </div>

                <div class="metric-small">
                    Income retained
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.write("")


    # =====================================================
    # FINANCIAL HEALTH + SMART INSIGHT
    # =====================================================

    col1, col2 = st.columns(
        [1, 1.7]
    )

    with col1:

        if selected_health_score >= 80:
            health_message = (
                "Your savings and spending pattern "
                "are currently in a strong range."
            )

        elif selected_health_score >= 60:
            health_message = (
                "Your finances are reasonably healthy, "
                "with room for further improvement."
            )

        elif selected_health_score >= 40:
            health_message = (
                "Your current numbers suggest that "
                "some spending habits deserve attention."
            )

        else:
            health_message = (
                "Your financial position needs attention. "
                "Start by reviewing your largest expenses."
            )

        st.markdown(
            f"""
            <div class="health-card">

                <div class="card-title">
                    Financial Health
                </div>

                <div class="card-subtitle">
                    A simple snapshot of your financial behaviour
                </div>

                <div class="health-score">
                    {selected_health_score}
                    <span style="
                        font-size:1rem;
                        color:#788594;
                    ">
                        / 100
                    </span>
                </div>

                <div class="health-label">
                    {selected_health_label}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(
            selected_health_score / 100
        )

        st.markdown(
            f"""
            <div class="health-tip">
                {health_message}
            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        if selected_balance < 0:

            insight = (
                "You're currently spending more than your recorded "
                "income. Your first priority should be identifying "
                "the categories contributing most to the gap."
            )

        elif selected_savings_rate < 20:

            insight = (
                "Your savings rate is below 20%. Consider reviewing "
                "recurring expenses and discretionary spending to "
                "create more room for savings."
            )

        elif selected_savings_rate < 40:

            insight = (
                "You're maintaining a moderate savings rate. "
                "Small improvements in your largest spending "
                "categories could strengthen your financial position."
            )

        else:

            insight = (
                "You're retaining a strong portion of your income. "
                "Continue tracking your spending so you can maintain "
                "this positive financial pattern."
            )

        st.markdown(
            f"""
            <div class="insight-card">

                <div class="insight-label">
                    ✦ Smart Insight
                </div>

                <div class="insight-text">
                    {insight}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.write("")


    # =====================================================
    # INTERACTIVE FINANCIAL TREND
    # =====================================================

    st.markdown(
        """
        <div class="section-label">
            Money Movement
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="card-subtitle">
            Hover over the chart to explore your income and expenses.
        </div>
        """,
        unsafe_allow_html=True
    )

    trend_chart = create_financial_chart(
        selected_incomes,
        selected_expenses
    )

    if trend_chart is not None:

        st.plotly_chart(
            trend_chart,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    else:

        st.info(
            "Add transactions to start building your financial story."
        )


    # =====================================================
    # SPENDING BREAKDOWN + MONEY STORY
    # =====================================================

    col1, col2 = st.columns(
        [1.1, 1]
    )

    with col1:

        st.markdown(
            """
            <div class="section-label">
                Where Your Money Goes
            </div>
            """,
            unsafe_allow_html=True
        )

        spending_chart = create_spending_chart(
            selected_expenses
        )

        if spending_chart is not None:

            st.plotly_chart(
                spending_chart,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        else:

            st.info(
                "Add expenses to see your spending breakdown."
            )


    with col2:

        highest_category, highest_amount = (
            find_highest_spending_category(
                selected_expenses
            )
        )

        if highest_category is not None:

            percentage = (
                highest_amount
                / selected_expense_total
                * 100
            ) if selected_expense_total > 0 else 0

            story_text = (
                f"Your biggest spending category is "
                f"<strong>{highest_category}</strong>, "
                f"accounting for approximately "
                f"<strong>{percentage:.1f}%</strong> of your "
                f"recorded spending."
            )

            if percentage >= 50:

                story_text += (
                    " This category has a major influence on "
                    "your financial position, so it may be "
                    "worth reviewing."
                )

            elif percentage >= 30:

                story_text += (
                    " Keeping an eye on this category could "
                    "help you improve your savings rate."
                )

            else:

                story_text += (
                    " Your spending appears reasonably "
                    "distributed across categories."
                )

        else:

            story_text = (
                "Once you start recording expenses, this section "
                "will tell the story behind your spending."
            )

        st.markdown(
            f"""
            <div class="story-card">

                <div class="story-title">
                    ✨ Your Money Story
                </div>

                <div class="story-text">
                    {story_text}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.write("")


        # Extra mini insight

        if selected_income_total > 0:

            expense_ratio = (
                selected_expense_total
                / selected_income_total
            ) * 100

            st.markdown(
                f"""
                <div class="content-card">

                    <div class="card-title">
                        Spending Efficiency
                    </div>

                    <div class="card-subtitle">
                        Percentage of income used for expenses
                    </div>

                    <div style="
                        font-size:2rem;
                        font-weight:750;
                        color:#f2f5f8;
                    ">
                        {expense_ratio:.1f}%
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    # =====================================================
    # RECENT TRANSACTIONS
    # =====================================================

    st.markdown(
        """
        <div class="section-label">
            Recent Activity
        </div>
        """,
        unsafe_allow_html=True
    )

    transactions = []

    for item in selected_incomes:

        transactions.append(
            {
                "date": item["date"],
                "name": item["source"],
                "type": "Income",
                "amount": item["amount"]
            }
        )

    for item in selected_expenses:

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
            "No transactions recorded for this period."
        )


    # =====================================================
    # QUICK ACTIONS
    # =====================================================

    st.markdown(
        """
        <div class="section-label">
            Quick Actions
        </div>
        """,
        unsafe_allow_html=True
    )

    action1, action2, action3, action4 = st.columns(4)

    with action1:

        if st.button(
            "＋ Add Transaction",
            use_container_width=True
        ):

            st.info(
                "Use the Add Transaction page from the sidebar."
            )

    with action2:

        if st.button(
            "▣ View History",
            use_container_width=True
        ):

            st.info(
                "Use the History page from the sidebar."
            )

    with action3:

        if st.button(
            "◈ Spending Analysis",
            use_container_width=True
        ):

            st.info(
                "Use the Spending Analysis page from the sidebar."
            )

    with action4:

        if st.button(
            "✦ AI Advisor",
            use_container_width=True
        ):

            st.info(
                "Use the AI Financial Advisor page from the sidebar."
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

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown(
                f"""
                <div class="metric-card metric-expense">

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
                <div class="metric-card metric-saving">

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

        col1, col2 = st.columns(
            [1.4, 1]
        )

        with col1:

            st.markdown(
                '<div class="section-label">Spending by Category</div>',
                unsafe_allow_html=True
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

            fig = px.bar(
                spending_df,
                x="Category",
                y="Amount",
                text_auto=".2s"
            )

            fig.update_layout(
                height=360,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="#aab4c0"
                ),
                xaxis=dict(
                    showgrid=False
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.06)",
                    tickprefix="₹"
                ),
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10
                )
            )

            fig.update_traces(
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Amount: ₹%{y:,.0f}"
                    "<extra></extra>"
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
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

    if st.button(
        "✦ Generate Financial Analysis",
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