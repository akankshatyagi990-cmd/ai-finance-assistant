# 💰 AI Finance Assistant

A modern personal finance management application built with Python and Streamlit.

The AI Finance Assistant helps users track their income and expenses, understand their spending patterns, manage monthly budgets, monitor financial health, perform financial calculations, and receive AI-powered financial guidance.

---

## 🚀 Project Overview

Managing personal finances often requires using multiple tools for tracking expenses, calculating loans, monitoring budgets, and understanding spending habits.

This project brings these functionalities together into one simple and interactive application.

The application combines:

- Financial tracking
- Data analysis
- Budget management
- Financial calculations
- Interactive dashboards
- AI-assisted financial guidance
- SQLite database storage

The goal is to create a practical finance application while applying Python, data analysis, database management, and AI/ML concepts.

---

## ✨ Features

### 📊 Financial Dashboard

The dashboard provides an overview of the user's financial activity.

It includes:

- Total income
- Total expenses
- Net balance
- Savings rate
- Financial health overview
- Financial insights
- Spending visualization
- Financial trends
- Recent transactions
- Monthly budget snapshot

---

### 💵 Income & Expense Tracking

Users can record their financial transactions.

#### Income

Users can add:

- Income source
- Amount
- Date

#### Expenses

Users can add:

- Expense category
- Amount
- Date

All transactions are stored in a SQLite database.

---

### 📋 Transaction History

The application maintains a history of recorded transactions.

Users can:

- View income records
- View expense records
- Review transaction dates
- Delete unwanted records

---

### 📈 Spending Analysis

The application analyzes spending patterns by category.

Users can understand:

- Where their money is being spent
- Category-wise spending
- Spending distribution
- Monthly spending patterns

Interactive charts are used to make the information easier to understand.

---

### 🎯 Budget Planner

Users can create monthly budgets for different spending categories.

The Budget Planner provides:

- Category-wise budgets
- Actual spending
- Remaining budget
- Budget utilization
- Budget status
- Budget vs Actual comparison

The dashboard also provides a quick budget snapshot for the selected month.

---

### 🧮 Financial Calculators

The application includes financial calculation tools such as:

- Simple Interest
- Compound Interest
- EMI Calculator

These tools help users perform common financial calculations without leaving the application.

---

### 🧠 Financial Insights

The application analyzes financial data and generates useful insights based on:

- Income
- Expenses
- Savings
- Spending patterns
- Budget utilization

The purpose is to convert raw financial data into information that users can understand more easily.

---

### ❤️ Financial Health

The application provides a financial health overview based on the user's financial activity.

It considers factors such as:

- Income
- Expenses
- Savings
- Spending behavior
- Budget performance

This gives users a quick view of their overall financial situation.

---

### 🤖 AI Financial Advisor

The application includes an AI-powered financial advisor component.

Users can use it to receive financial guidance based on the information provided to the application.

The AI component is designed to demonstrate how AI can be integrated into a personal finance application.

> Note: AI functionality may depend on the availability and configuration of the selected AI API.

---

## 🛠️ Technology Stack

### Programming Language

- Python

### User Interface

- Streamlit

### Data Analysis

- Pandas

### Visualization

- Plotly

### Database

- SQLite

### AI

- Generative AI / LLM integration

### Development Tools

- Visual Studio Code
- Git
- GitHub

---

## 🏗️ Project Structure

```text
AI-Finance-Assistant/
│
├── app/
│   ├── main.py
│   ├── finance.py
│   ├── expense_tracker.py
│   ├── income_tracker.py
│   ├── financial_summary.py
│   ├── financial_advisor.py
│   ├── spending_analysis.py
│   ├── ai_advisor.py
│   ├── database.py
│   ├── financial_insights.py
│   ├── financial_health.py
│   ├── web_app.py
│   └── budget.py
│
├── README.md
│
└── finance.db
