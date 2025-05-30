Below is the complete code that integrates the functions for gamification, rewards, risk profiling, investment suggestions, and intelligent savings into the existing Streamlit application. This code assumes that you have the necessary context and structure from the original code you provided.

```python
# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
from datetime import datetime, timedelta
import random
from sklearn.linear_model import LinearRegression
import time

# Set page configuration
st.set_page_config(
    page_title="neuro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define improved color scheme
PRIMARY_COLOR = "#4A90E2"  # Blue
SECONDARY_COLOR = "#F5F5F5"  # Light Gray
ACCENT_COLOR = "#50E3C2"  # Teal
TEXT_COLOR = "#333333"  # Dark Gray
LIGHT_TEXT = "#FFFFFF"  # White

# Apply custom CSS
st.markdown(f"""
<style>
    .main .block-container {{
        padding-top: 1rem;
        padding-bottom: 1rem;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {TEXT_COLOR};
        font-weight: 600;
    }}
    .stButton>button {{
        background-color: {PRIMARY_COLOR};
        color: {LIGHT_TEXT};
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }}
    .stButton>button:hover {{
        background-color: {PRIMARY_COLOR}CC;
    }}
    .highlight-card {{
        background-color: {PRIMARY_COLOR};
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
    }}
    .secondary-card {{
        background-color: {SECONDARY_COLOR};
        padding: 1.5rem;
        border-radius: 10px;
    }}
    .css-1d391kg {{
        background-color: {PRIMARY_COLOR};
    }}
    .subscription-card {{
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }}
    .basic-card {{ background-color: #f8f9fa; }}
    .pro-card {{ background-color: #e8eaf6; }}
    .elite-card {{ background-color: #e3f2fd; }}

    /* Custom CSS for rounded buttons */
    .rounded-button {{
        background-color: #f0f0f0;
        border-radius: 20px;
        padding: 10px 15px;
        margin: 5px;
        display: inline-block;
        text-align: center;
        cursor: pointer;
    }}

    /* Custom progress bar */
    .progress-container {{
        width: 100%;
        background-color: #e0e0e0;
        border-radius: 5px;
        margin-bottom: 10px;
    }}
    .progress-bar {{
        height: 10px;
        border-radius: 5px;
        text-align: center;
    }}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'login_status' not in st.session_state:
    st.session_state.login_status = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'
if 'subscription' not in st.session_state:
    st.session_state.subscription = 'Basic'  # Default subscription
if 'balance' not in st.session_state:
    st.session_state.balance = 0.0
if 'savings' not in st.session_state:
    st.session_state.savings = 0.0
if 'investments' not in st.session_state:
    st.session_state.investments = 0.0
if 'goals' not in st.session_state:
    st.session_state.goals = []
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["date", "category", "amount", "description", "type"])
if 'insights' not in st.session_state:
    st.session_state.insights = []
if 'roundups' not in st.session_state:
    st.session_state.roundups = 0.0  # Amount accumulated from round-ups
if 'first_login' not in st.session_state:
    st.session_state.first_login = True
if 'rewards' not in st.session_state:
    st.session_state.rewards = 0
if 'risk_profile' not in st.session_state:
    st.session_state.risk_profile = None

# Navigation function
def navigate_to(page):
    st.session_state.current_page = page

# Authentication functions
def login():
    st.markdown("<h1 style='text-align: center;'>neuro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Your AI-powered financial companion</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='padding: 2rem; background-color: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>", unsafe_allow_html=True)
        username = st.text_input("Email or Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username and password:  # Simple validation
                st.session_state.login_status = True

                # If this is the first login, navigate to the onboarding page
                if st.session_state.first_login:
                    st.session_state.current_page = 'onboarding'
                else:
                    st.session_state.current_page = 'dashboard'

                st.rerun()
            else:
                st.error("Please enter both username and password")

        st.markdown("<div style='text-align: center; margin-top: 1rem;'>", unsafe_allow_html=True)
        st.markdown("<a href='#' style='color: #4A90E2; text-decoration: none;'>Forgot password?</a>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='text-align: center; margin-top: 1rem;'>", unsafe_allow_html=True)
        st.markdown("Don't have an account? <a href='#' style='color: #4A90E2; text-decoration: none;'>Sign up</a>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Onboarding function for new users
def onboarding():
    st.markdown("<h1 style='text-align: center;'>Welcome to neuro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Let's set up your financial profile</p>", unsafe_allow_html=True)

    # Create tabs for each step of the onboarding process
    tab1, tab2, tab3 = st.tabs(["Basic Information", "Financial Data", "Goals"])

    with tab1:
        st.header("Basic Information")

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Full Name", key="full_name")
            st.text_input("Email", key="email")

        with col2:
            st.selectbox("Currency", ["EUR (€)", "USD ($)", "GBP (£)", "JPY (¥)"], key="currency")
            st.selectbox("Income Frequency", ["Monthly", "Bi-weekly", "Weekly"], key="income_frequency")

    with tab2:
        st.header("Financial Data")

        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Current Account Balance", value=0.0, step=100.0, key="initial_balance")
            st.number_input("Savings", value=0.0, step=100.0, key="initial_savings")

        with col2:
            st.number_input("Investments", value=0.0, step=100.0, key="initial_investments")
            st.number_input("Monthly Income", value=0.0, step=100.0, key="monthly_income")

        # Form for adding transactions
        st.subheader("Add Your Recent Transactions")

        with st.form("add_transactions_form"):
            st.info("Add your most recent transactions to get started. You can add more later.")

            transaction_date = st.date_input("Date", value=datetime.now())
            transaction_category = st.selectbox("Category", ["Income", "Groceries", "Dining", "Entertainment", "Transport", "Shopping", "Utilities", "Other"])
            transaction_amount = st.number_input("Amount", value=0.0, step=10.0)
            transaction_description = st.text_input("Description")

            submit_button = st.form_submit_button("Add Transaction")

            if submit_button:
                # Determine transaction type
                tx_type = "income" if transaction_category == "Income" else "expense"
                tx_amount = transaction_amount if tx_type == "income" else -transaction_amount

                # Create a new row for the transaction
                new_tx = pd.DataFrame({
                    "date": [transaction_date.strftime("%Y-%m-%d")],
                    "category": [transaction_category],
                    "amount": [tx_amount],
                    "description": [transaction_description],
                    "type": [tx_type]
                })

                # Append to existing transactions or create a new DataFrame
                if st.session_state.transactions.empty:
                    st.session_state.transactions = new_tx
                else:
                    st.session_state.transactions = pd.concat([st.session_state.transactions, new_tx], ignore_index=True)

                st.success("Transaction added!")

        # Display added transactions
        if not st.session_state.transactions.empty:
            st.subheader("Your Added Transactions")
            st.dataframe(st.session_state.transactions[["date", "category", "amount", "description"]])

    with tab3:
        st.header("Financial Goals")

        st.info("Set up your financial goals to help us provide better insights.")

        with st.form("add_goal_form"):
            goal_name = st.text_input("Goal Name", placeholder="e.g., Emergency Fund, New Car, Vacation")
            goal_target = st.number_input("Target Amount (€)", min_value=1.0, value=1000.0)
            goal_current = st.number_input("Current Amount (€)", min_value=0.0, value=0.0)
            goal_date = st.date_input("Target Date", value=datetime.now() + timedelta(days=365))

            submit_goal = st.form_submit_button("Add Goal")

            if submit_goal and goal_name:
                # Add the goal to session state
                new_goal = {
                    "name": goal_name,
                    "target": goal_target,
                    "current": goal_current,
                    "date": goal_date.strftime("%Y-%m-%d")
                }

                st.session_state.goals.append(new_goal)
                st.success(f"Goal '{goal_name}' added!")

        # Display added goals
        if st.session_state.goals:
            st.subheader("Your Goals")
            for i, goal in enumerate(st.session_state.goals):
                progress = (goal["current"] / goal["target"]) * 100

                st.markdown(f"""
                <div style="padding: 1rem; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin: 0;">{goal["name"]}</h3>
                        <span style="font-weight: 500;">€{goal["current"]:.0f} / €{goal["target"]:.0f}</span>
                    </div>
                    <div class="progress-container" style="margin-top: 0.5rem;">
                        <div class="progress-bar" style="width: {progress}%; background-color: {PRIMARY_COLOR}"></div>
                    </div>
                    <p style="margin-top: 0.5rem;">Target date: {goal["date"]}</p>
                </div>
                """, unsafe_allow_html=True)

    # Complete onboarding button
    if st.button("Complete Setup"):
        # Update session state with onboarding data
        if "initial_balance" in st.session_state:
            st.session_state.balance = st.session_state.initial_balance
        if "initial_savings" in st.session_state:
            st.session_state.savings = st.session_state.initial_savings
        if "initial_investments" in st.session_state:
            st.session_state.investments = st.session_state.initial_investments

        # Generate insights based on user data
        st.session_state.insights = generate_insights()

        # Mark first login as complete
        st.session_state.first_login = False

        # Navigate to dashboard
        st.session_state.current_page = 'dashboard'
        st.rerun()

# Function to generate insights based on user data
def generate_insights():
    insights = []

    # Only generate insights if we have transactions
    if not st.session_state.transactions.empty:
        expenses = st.session_state.transactions[st.session_state.transactions['type'] == 'expense']
        if not expenses.empty:
            # Most expensive category
            expense_by_category = expenses.groupby('category')['amount'].sum().abs()
            if not expense_by_category.empty:
                top_category = expense_by_category.idxmax()
                top_amount = expense_by_category.max()
                insights.append(f"Your highest spending category is {top_category} (€{top_amount:.2f}).")

        # If we have income transactions
        income = st.session_state.transactions[st.session_state.transactions['type'] == 'income']
        if not income.empty:
            total_income = income['amount'].sum()
            total_expenses = expenses['amount'].sum().abs() if not expenses.empty else 0

            if total_income > 0:
                savings_rate = ((total_income - total_expenses) / total_income) * 100
                insights.append(f"Your current savings rate is {savings_rate:.1f}%.")

    # Add insights based on goals
    if st.session_state.goals:
        for goal in st.session_state.goals:
            progress = (goal["current"] / goal["target"]) * 100
            insights.append(f"Your {goal['name']} goal is {progress:.1f}% complete.")

    # Add default insights if we don't have enough
    if len(insights) < 3:
        default_insights = [
            "Starting to track your expenses is the first step to financial freedom.",
            "Consider setting up an emergency fund equal to 3-6 months of expenses.",
            "Regularly reviewing your spending patterns can help identify savings opportunities."
        ]

        for insight in default_insights:
            if len(insights) < 3:
                insights.append(insight)

    return insights[:3]  # Return at most 3 insights

# Function to predict future expenses using a simple linear regression model
def predict_future_expenses():
    if not st.session_state.transactions.empty:
        # Prepare data for prediction
        transactions_df = st.session_state.transactions.copy()
        transactions_df['date'] = pd.to_datetime(transactions_df['date'])
        transactions_df['month'] = transactions_df['date'].dt.to_period('M').astype(str)

        # Group by month and sum expenses
        monthly_expenses = transactions_df[transactions_df['type'] == 'expense'].groupby('month')['amount'].sum().reset_index()
        monthly_expenses['amount'] = monthly_expenses['amount'].abs()  # Make sure amounts are positive

        # Create a numerical month index for regression
        monthly_expenses['month_index'] = np.arange(len(monthly_expenses))

        # Train a linear regression model
        model = LinearRegression()
        model.fit(monthly_expenses[['month_index']], monthly_expenses['amount'])

        # Predict next 3 months
        future_months = np.array([[len(monthly_expenses) + i] for i in range(1, 4)])
        predictions = model.predict(future_months)

        return predictions
    return None

# Function to track rewards
def track_rewards():
    # Example criteria for rewards
    if st.session_state.balance > 1000:
        st.session_state.rewards += 10  # Reward for maintaining a balance over €1000
        st.success("You've earned 10 rewards points for maintaining a balance over €1000!")

    if len(st.session_state.transactions) > 5:
        st.session_state.rewards += 5  # Reward for adding more than 5 transactions
        st.success("You've earned 5 rewards points for adding more than 5 transactions!")

    # Display total rewards
    st.markdown(f"Total Rewards Points: {st.session_state.rewards}")

# Function to assess risk profile
def assess_risk_profile():
    # Simple risk assessment based on savings and investments
    if st.session_state.investments > st.session_state.savings * 2:
        st.session_state.risk_profile = "High Risk"
    elif st.session_state.investments > st.session_state.savings:
        st.session_state.risk_profile = "Medium Risk"
    else:
        st.session_state.risk_profile = "Low Risk"

    st.markdown(f"Your Risk Profile: {st.session_state.risk_profile}")

# Function to provide investment suggestions
def provide_investment_suggestions():
    if st.session_state.risk_profile == "High Risk":
        st.markdown("**Suggested Investments:**")
        st.markdown("- Tech Stocks")
        st.markdown("- Cryptocurrency")
    elif st.session_state.risk_profile == "Medium Risk":
        st.markdown("**Suggested Investments:**")
        st.markdown("- Balanced Mutual Funds")
        st.markdown("- Index Funds")
    else:
        st.markdown("**Suggested Investments:**")
        st.markdown("- Government Bonds")
        st.markdown("- High-Interest Savings Accounts")

# Function to suggest savings goals
def suggest_savings_goals():
    if st.session_state.savings < 1000:
        st.markdown("**Savings Goal Suggestion:**")
        st.markdown("Consider setting a goal to save at least €1000 for emergencies.")
    elif st.session_state.savings < 5000:
        st.markdown("**Savings Goal Suggestion:**")
        st.markdown("Aim to save €5000 for a more secure emergency fund.")
    else:
        st.markdown("**Savings Goal Suggestion:**")
        st.markdown("Great job! Consider investing your savings for better returns.")

# Function for intelligent savings and investment suggestions
def intelligent_savings_investment():
    if st.button("Get Intelligent Savings and Investment Suggestions"):
        assess_risk_profile()
        provide_investment_suggestions()
        suggest_savings_goals()

# Dashboard components
def display_dashboard():
    st.markdown("<h2>Dashboard</h2>", unsafe_allow_html=True)

    # Call the rewards tracking function
    track_rewards()

    # Call the intelligent savings and investment suggestions function
    intelligent_savings_investment()

    # Top action: Add transaction button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("➕ Add New Transaction", key="add_tx_btn_dashboard"):
            navigate_to("transactions")
            st.rerun()

    # Top cards section
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="highlight-card">
            <h4 style="margin-top: 0;">Total Balance</h4>
            <h2 style="margin: 0;">€{st.session_state.balance:.2f}</h2>
            <p>Available funds</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="secondary-card">
            <h4 style="margin-top: 0;">Savings</h4>
            <h2 style="margin: 0;">€{st.session_state.savings:.2f}</h2>
            <p>Growing at 3.5% APY</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="secondary-card">
            <h4 style="margin-top: 0;">Investments</h4>
            <h2 style="margin: 0;">€{st.session_state.investments:.2f}</h2>
            <p>+5.2% this month</p>
        </div>
        """, unsafe_allow_html=True)

    # Round-up savings feature
    st.markdown("<h3>Round-up Savings</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"""
        <div style="padding: 1rem; background-color: #f8f9fa; border-radius: 10px;">
            <h4 style="margin-top: 0;">Round-up Savings</h4>
            <p>We round up your transactions and save the difference.</p>
            <div class="progress-container">
                <div class="progress-bar" style="width: 65%; background-color: {PRIMARY_COLOR}"></div>
            </div>
            <p>€{st.session_state.roundups:.2f} saved this month through round-ups</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='height: 100%; display: flex; align-items: center; justify-content: center;'>", unsafe_allow_html=True)
        if st.button("Boost Round-up"):
            st.session_state.roundups += 5.0
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # Recent transactions and spending analysis
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("<h3>Recent Transactions</h3>", unsafe_allow_html=True)

        if not st.session_state.transactions.empty:
            recent_transactions = st.session_state.transactions.sort_values(by="date", ascending=False).head(5)

            for _, tx in recent_transactions.iterrows():
                sign = "+" if tx["amount"] > 0 else "-"
                color = ACCENT_COLOR if tx["amount"] > 0 else TEXT_COLOR

                st.markdown(f"""
                <div style="padding: 0.75rem; border-bottom: 1px solid #e0e0e0; display: flex; justify-content: space-between;">
                    <div>
                        <p style="margin: 0; font-weight: 500;">{tx["description"]}</p>
                        <p style="margin: 0; color: gray; font-size: 0.8rem;">{tx["date"]} • {tx["category"]}</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-weight: 500; color: {color};">{sign}€{abs(tx["amount"]):.2f}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No transactions yet. Add your first transaction to see it here.")

        if st.button("See All Transactions"):
            navigate_to("transactions")
            st.rerun()

    with col2:
        st.markdown("<h3>Spending Analysis</h3>", unsafe_allow_html=True)

        # Prepare data for the chart
        if not st.session_state.transactions.empty:
            expense_data = st.session_state.transactions[st.session_state.transactions["type"] == "expense"]

            if not expense_data.empty:
                category_spending = expense_data.groupby("category")["amount"].sum().abs().reset_index()

                fig = px.pie(
                    category_spending,
                    values="amount",
                    names="category",
                    hole=0.4,
                    color_discrete_sequence=px.colors.sequential.Purples_r
                )
                fig.update_layout(margin=dict(t=0, b=0, l=20, r=20), height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Add expense transactions to see your spending analysis.")
        else:
            st.info("No transaction data available. Add transactions to view your spending analysis.")

    # AI Insights
    st.markdown("<h3>AI Financial Insights</h3>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    for i, (col, insight) in enumerate(zip([col1, col2, col3], st.session_state.insights)):
        with col:
            st.markdown(f"""
            <div style="padding: 1rem; background-color: #f8f9fa; border-radius: 10px; height: 100%;">
                <p style="margin: 0;">{insight}</p>
            </div>
            """, unsafe_allow_html=True)

    # Predict future expenses
    st.markdown("<h3>Future Expense Predictions</h3>", unsafe_allow_html=True)
    predictions = predict_future_expenses()
    if predictions is not None:
        st.write("Predicted expenses for the next 3 months:")
        for i, prediction in enumerate(predictions, start=1):
            st.write(f"Month {i}: €{prediction:.2f}")
    else:
        st.info("Not enough data to make predictions.")

    # Financial Goals
    st.markdown("<h3>Financial Goals</h3>", unsafe_allow_html=True)

    if st.session_state.goals:
        col1, col2 = st.columns(2)

        for i, goal in enumerate(st.session_state.goals):
            progress = (goal["current"] / goal["target"]) * 100
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"""
                <div style="padding: 1rem; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 1rem;">
                    <h4 style="margin-top: 0;">{goal["name"]}</h4>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {progress}%; background-color: {PRIMARY_COLOR}"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>€{goal["current"]:.0f}</span>
                        <span>€{goal["target"]:.0f}</span>
                    </div>
                    <p style="margin-top: 0.5rem; font-size: 0.9rem;">Target date: {goal["date"]}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No goals set yet. Add your first financial goal to track your progress.")

    if st.button("Add New Goal"):
        navigate_to("goals")
        st.rerun()

# Savings and Investments components
def display_savings():
    st.markdown("<h2>Savings & Investments</h2>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Savings", "Investments"])

    with tab1:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"""
            <div class="highlight-card">
                <h4 style="margin-top: 0;">Total Savings</h4>
                <h2 style="margin: 0;">€{st.session_state.savings:.2f}</h2>
                <p>Growing at 3.5% APY</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<h3>Update Savings</h3>", unsafe_allow_html=True)

            with st.form("update_savings"):
                new_savings = st.number_input("Current Savings Amount", value=st.session_state.savings, min_value=0.0, step=100.0)
                submit_savings = st.form_submit_button("Update Savings")

                if submit_savings:
                    st.session_state.savings = new_savings
                    st.success("Savings updated successfully!")
                    st.rerun()

        with col2:
            st.markdown("<h3>Automated Savings</h3>", unsafe_allow_html=True)

            auto_save_amount = st.number_input("Auto-save amount (€ / month)", min_value=0.0, value=100.0, step=25.0)

            st.markdown("<h4>Round-up Settings</h4>", unsafe_allow_html=True)

            roundup_multiplier = st.select_slider(
                "Round-up multiplier",
                options=[1, 2, 3, 5, 10],
                value=1
            )

            if st.button("Save Settings"):
                st.success("Savings settings updated successfully!")

            st.markdown(f"""
            <div style="padding: 1rem; background-color: #f8f9fa; border-radius: 10px; margin-top: 1rem;">
                <h4 style="margin-top: 0;">Current Round-ups</h4>
                <h3 style="margin: 0;">€{st.session_state.roundups:.2f}</h3>
                <p>Saved this month</p>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        if st.session_state.subscription in ['Pro', 'Elite']:
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"""
                <div class="highlight-card">
                    <h4 style="margin-top: 0;">Total Investments</h4>
                    <h2 style="margin: 0;">€{st.session_state.investments:.2f}</h2>
                    <p>+5.2% this month</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<h3>Update Investments</h3>", unsafe_allow_html=True)

                with st.form("update_investments"):
                    new_investments = st.number_input("Current Investment Amount", value=st.session_state.investments, min_value=0.0, step=100.0)
                    submit_investments = st.form_submit_button("Update Investments")

                    if submit_investments:
                        st.session_state.investments = new_investments
                        st.success("Investments updated successfully!")
                        st.rerun()

            with col2:
                st.markdown("<h3>AI Investment Suggestions</h3>", unsafe_allow_html=True)

                st.markdown("""
                <div style="padding: 1rem; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 1rem;">
                    <h4 style="margin-top: 0;">Suggested ETF</h4>
                    <p style="margin: 0; font-weight: 500;">Vanguard FTSE All-World</p>
                    <p style="margin: 0; color: green;">+7.2% YTD</p>
                    <p style="margin-top: 0.5rem; font-size: 0.9rem;">Global diversification with low fees</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div style="padding: 1rem; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 1rem;">
                    <h4 style="margin-top: 0;">Portfolio Suggestion</h4>
                    <p style="margin: 0;">Based on your risk profile:</p>
                    <ul style="margin-top: 0.5rem;">
                        <li>70% Global Equities</li>
                        <li>20% Bonds</li>
                        <li>10% Alternatives</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

                if st.button("Get Custom Investment Plan"):
                    st.info("Our AI is preparing your custom investment plan...")
                    with st.spinner("Analyzing market conditions..."):
                        time.sleep(2)
                    st.success("Your custom investment plan is ready!")

        else:
            st.warning("Upgrade to Pro or Elite to access AI-driven investment suggestions and portfolio management.")
            if st.button("Upgrade Subscription"):
                navigate_to("subscription")
                st.rerun()

# Transactions and analysis components
def display_transactions():
    st.markdown("<h2>Transactions & Analysis</h2>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Transactions", "Cash Flow Analysis"])

    with tab1:
        # Add transaction form
        st.subheader("Add New Transaction")

        with st.form("add_transaction_form"):
            col1, col2 = st.columns(2)

            with col1:
                transaction_date = st.date_input("Date", value=datetime.now())
                transaction_category = st.selectbox(
                    "Category",
                    ["Income", "Groceries", "Dining", "Entertainment", "Transport", "Shopping", "Utilities", "Other"]
                )

            with col2:
                transaction_amount = st.number_input("Amount", value=0.0, step=10.0)
                transaction_description = st.text_input("Description")
                            submit_tx = st.form_submit_button("Add Transaction")

            if submit_tx:
                # Determine transaction type
                tx_type = "income" if transaction_category == "Income" else "expense"
                tx_amount = transaction_amount if tx_type == "income" else -transaction_amount

                # Create a new row for the transaction
                new_tx = pd.DataFrame({
                    "date": [transaction_date.strftime("%Y-%m-%d")],
                    "category": [transaction_category],
                    "amount": [tx_amount],
                    "description": [transaction_description],
                    "type": [tx_type]
                })

                # Append to existing transactions or create a new DataFrame
                if st.session_state.transactions.empty:
                    st.session_state.transactions = new_tx
                else:
                    st.session_state.transactions = pd.concat([st.session_state.transactions, new_tx], ignore_index=True)

                # Update balance
                if tx_type == "income":
                    st.session_state.balance += transaction_amount
                else:
                    st.session_state.balance -= transaction_amount

                # Update roundups for expenses
                if tx_type == "expense":
                    cents = transaction_amount % 1
                    if cents > 0:
                        roundup = 1 - cents
                        st.session_state.roundups += roundup

                st.success("Transaction added successfully!")
                st.rerun()

        # Transaction filters
        st.subheader("Transaction History")

        col1, col2, col3 = st.columns(3)

        with col1:
            filter_start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))

        with col2:
            filter_end_date = st.date_input("End Date", value=datetime.now())

        with col3:
            filter_category = st.multiselect(
                "Categories",
                ["All"] + ["Income", "Groceries", "Dining", "Entertainment", "Transport", "Shopping", "Utilities", "Other"],
                default=["All"]
            )

        # Apply filters
        if not st.session_state.transactions.empty:
            filtered_transactions = st.session_state.transactions.copy()

            # Convert date strings to datetime objects for comparison
            filtered_transactions['date'] = pd.to_datetime(filtered_transactions['date'])

            # Date filter
            mask = (filtered_transactions['date'] >= pd.Timestamp(filter_start_date)) & \
                   (filtered_transactions['date'] <= pd.Timestamp(filter_end_date))
            filtered_transactions = filtered_transactions[mask]

            # Category filter
            if "All" not in filter_category:
                filtered_transactions = filtered_transactions[filtered_transactions['category'].isin(filter_category)]

            # Display filtered transactions
            if not filtered_transactions.empty:
                # Convert dates back to string for display
                display_transactions = filtered_transactions.copy()
                display_transactions['date'] = display_transactions['date'].dt.strftime('%Y-%m-%d')

                st.dataframe(
                    display_transactions[["date", "category", "amount", "description"]],
                    use_container_width=True,
                    hide_index=True
                )

                # Add download option
                csv = display_transactions.to_csv(index=False)
                st.download_button(
                    label="Download Transactions",
                    data=csv,
                    file_name="neuro_transactions.csv",
                    mime="text/csv"
                )
            else:
                st.info("No transactions match your filter criteria.")
        else:
            st.info("No transactions available. Add your first transaction above.")

    with tab2:
        if not st.session_state.transactions.empty:
            # Prepare data for cash flow analysis
            st.subheader("Monthly Cash Flow")

            # Convert date to datetime if it's not already
            transactions_df = st.session_state.transactions.copy()
            transactions_df['date'] = pd.to_datetime(transactions_df['date'])

            # Extract month for grouping
            transactions_df['month'] = transactions_df['date'].dt.strftime('%Y-%m')

            # Group by month and transaction type
            monthly_flow = transactions_df.groupby(['month', 'type'])['amount'].sum().reset_index()

            # Pivot to get income and expenses side by side
            pivot_df = monthly_flow.pivot_table(
                index='month',
                columns='type',
                values='amount',
                aggfunc='sum'
            ).reset_index().fillna(0)

            # Make sure both columns exist
            if 'income' not in pivot_df.columns:
                pivot_df['income'] = 0
            if 'expense' not in pivot_df.columns:
                pivot_df['expense'] = 0

            # Calculate net flow
            pivot_df['net'] = pivot_df['income'] + pivot_df['expense']  # expense is already negative

            # Create the cash flow chart
            fig = px.bar(
                pivot_df,
                x='month',
                y=['income', 'expense', 'net'],
                barmode='group',
                title='Monthly Income vs Expenses',
                color_discrete_map={
                    'income': ACCENT_COLOR,
                    'expense': '#FF5252',  # Red for expenses
                    'net': PRIMARY_COLOR
                }
            )

            fig.update_layout(legend_title_text='Type', height=400)
            st.plotly_chart(fig, use_container_width=True)

            # Category breakdown
            st.subheader("Expense Breakdown by Category")

            # Filter for expenses only
            expenses = transactions_df[transactions_df['type'] == 'expense']

            if not expenses.empty:
                # Group by category
                category_expenses = expenses.groupby('category')['amount'].sum().abs().reset_index()
                category_expenses = category_expenses.sort_values('amount', ascending=False)

                fig = px.bar(
                    category_expenses,
                    x='category',
                    y='amount',
                    title='Total Spending by Category',
                    color='amount',
                    color_continuous_scale='Purples'
                )

                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

                # Spending trends over time
                st.subheader("Spending Trends")

                # Group by month and category
                category_month = expenses.groupby(['month', 'category'])['amount'].sum().abs().reset_index()

                fig = px.line(
                    category_month,
                    x='month',
                    y='amount',
                    color='category',
                    title='Monthly Spending by Category'
                )

                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No expense transactions available for analysis.")
        else:
            st.info("Add transactions to see your cash flow analysis.")

# Financial goals components
def display_goals():
    st.markdown("<h2>Financial Goals</h2>", unsafe_allow_html=True)

    # Add new goal form
    st.subheader("Add New Goal")

    with st.form("add_new_goal"):
        col1, col2 = st.columns(2)

        with col1:
            goal_name = st.text_input("Goal Name", placeholder="e.g., Emergency Fund, New Car, Vacation")
            goal_target = st.number_input("Target Amount (€)", min_value=1.0, value=1000.0)

        with col2:
            goal_current = st.number_input("Current Amount (€)", min_value=0.0, value=0.0)
            goal_date = st.date_input("Target Date", value=datetime.now() + timedelta(days=365))

        submit_new_goal = st.form_submit_button("Add Goal")

        if submit_new_goal and goal_name:
            # Add the goal to session state
            new_goal = {
                "name": goal_name,
                "target": goal_target,
                "current": goal_current,
                "date": goal_date.strftime("%Y-%m-%d")
            }

            st.session_state.goals.append(new_goal)
            st.success(f"Goal '{goal_name}' added!")
            st.rerun()

    # Display existing goals
    if st.session_state.goals:
        st.subheader("Your Financial Goals")

        for i, goal in enumerate(st.session_state.goals):
            progress = (goal["current"] / goal["target"]) * 100
            months_to_target = None

            # Calculate time to target
            if goal["date"]:
                target_date = datetime.strptime(goal["date"], "%Y-%m-%d")
                today = datetime.now()
                days_to_target = (target_date - today).days
                months_to_target = max(days_to_target / 30, 0)

            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.markdown(f"""
                <div style="padding: 1rem; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 1rem;">
                    <h3 style="margin-top: 0;">{goal["name"]}</h3>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {progress}%; background-color: {PRIMARY_COLOR}"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                        <span>Current: €{goal["current"]:.2f}</span>
                        <span>Target: €{goal["target"]:.2f}</span>
                    </div>
                    <p style="margin-top: 0.5rem;">Target date: {goal["date"]}</p>
                    """, unsafe_allow_html=True)

                if months_to_target is not None and months_to_target > 0:
                    monthly_contribution = (goal["target"] - goal["current"]) / months_to_target
                    st.markdown(f"""
                    <p>Suggested monthly contribution: <strong>€{monthly_contribution:.2f}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                if st.button(f"Update", key=f"update_goal_{i}"):
                    st.session_state.editing_goal = i
                    st.rerun()

            with col3:
                if st.button(f"Delete", key=f"delete_goal_{i}"):
                    st.session_state.goals.pop(i)
                    st.success("Goal deleted successfully!")
                    st.rerun()

        # Goal editing form (appears when Update is clicked)
        if 'editing_goal' in st.session_state and st.session_state.editing_goal is not None:
            i = st.session_state.editing_goal
            goal = st.session_state.goals[i]

            st.subheader(f"Update Goal: {goal['name']}")

            with st.form(f"update_goal_form_{i}"):
                updated_name = st.text_input("Goal Name", value=goal["name"])
                updated_target = st.number_input("Target Amount (€)", value=goal["target"], min_value=1.0)
                updated_current = st.number_input("Current Amount (€)", value=goal["current"], min_value=0.0)
                updated_date = st.date_input("Target Date", value=datetime.strptime(goal["date"], "%Y-%m-%d"))

                col1, col2 = st.columns(2)

                with col1:
                    update_button = st.form_submit_button("Save Changes")

                with col2:
                    if st.form_submit_button("Cancel"):
                        st.session_state.editing_goal = None
                        st.rerun()

                if update_button:
                    # Update the goal
                    st.session_state.goals[i] = {
                        "name": updated_name,
                        "target": updated_target,
                        "current": updated_current,
                        "date": updated_date.strftime("%Y-%m-%d")
                    }

                    st.success("Goal updated successfully!")
                    st.session_state.editing_goal = None
                    st.rerun()
    else:
        st.info("No goals set yet. Add your first financial goal using the form above.")

# Subscription management
def display_subscription():
    st.markdown("<h2>Subscription Management</h2>", unsafe_allow_html=True)

    st.markdown("""
    <p>Choose the plan that fits your financial journey. Upgrade anytime to unlock more features.</p>
    """, unsafe_allow_html=True)

    # Display subscription cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="subscription-card basic-card">
            <h3>Basic</h3>
            <h2>€0/month</h2>
            <p>Start your financial journey</p>
            <hr>
            <ul>
                <li>Expense tracking</li>
                <li>Basic financial insights</li>
                <li>Goal setting</li>
                <li>Unlimited transactions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.subscription != "Basic":
            if st.button("Downgrade to Basic"):
                st.session_state.subscription = "Basic"
                st.success("Subscription updated to Basic!")
                st.rerun()
        else:
            st.info("Current Plan")

    with col2:
        st.markdown("""
        <div class="subscription-card pro-card">
            <h3>Pro</h3>
            <h2>€4.99/month</h2>
            <p>Advanced insights and planning</p>
            <hr>
            <ul>
                <li>Everything in Basic</li>
                <li>AI-powered insights</li>
                <li>Investment tracking</li>
                <li>Advanced analytics</li>
                <li>Goal recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.subscription != "Pro":
            if st.button("Upgrade to Pro"):
                st.session_state.subscription = "Pro"
                st.success("Subscription updated to Pro!")
                st.rerun()
        else:
            st.info("Current Plan")

    with col3:
        st.markdown("""
        <div class="subscription-card elite-card">
            <h3>Elite</h3>
            <h2>€9.99/month</h2>
            <p>Personalized financial assistant</p>
            <hr>
            <ul>
                <li>Everything in Pro</li>
                <li>Custom investment strategies</li>
                <li>Priority AI assistance</li>
                <li>Tax optimization</li>
                <li>Financial advisor chat</li>
                <li>Unlimited goal coaching</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.subscription != "Elite":
            if st.button("Upgrade to Elite"):
                st.session_state.subscription = "Elite"
                st.success("Subscription updated to Elite!")
                st.rerun()
        else:
            st.info("Current Plan")

# Profile and settings
def display_profile():
    st.markdown("<h2>Profile & Settings</h2>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Profile", "Settings"])

    with tab1:
        col1, col2 = st.columns([1, 3])

        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150)
            if st.button("Change Photo"):
                st.info("Feature coming soon!")

        with col2:
            if 'full_name' not in st.session_state:
                st.session_state.full_name = ""
            if 'email' not in st.session_state:
                st.session_state.email = ""

            st.markdown("<h3>Personal Information</h3>", unsafe_allow_html=True)

            with st.form("update_profile"):
                full_name = st.text_input("Full Name", value=st.session_state.full_name)
                email = st.text_input("Email", value=st.session_state.email)
                phone = st.text_input("Phone")

                st.markdown("<h4>Financial Profile</h4>", unsafe_allow_html=True)

                col1, col2 = st.columns(2)

                with col1:
                    currency = st.selectbox(
                        "Currency",
                        ["EUR (€)", "USD ($)", "GBP (£)", "JPY (¥)"],
                        index=0 if 'currency' not in st.session_state else ["EUR (€)", "USD ($)", "GBP (£)", "JPY (¥)"].index(st.session_state.currency)
                    )

                with col2:
                    income_frequency = st.selectbox(
                        "Income Frequency",
                        ["Monthly", "Bi-weekly", "Weekly"],
                        index=0 if 'income_frequency' not in st.session_state else ["Monthly", "Bi-weekly", "Weekly"].index(st.session_state.income_frequency)
                    )

                submit_profile = st.form_submit_button("Save Changes")

                if submit_profile:
                    st.session_state.full_name = full_name
                    st.session_state.email = email
                    st.session_state.currency = currency
                    st.session_state.income_frequency = income_frequency
                    st.success("Profile updated successfully!")

    with tab2:
        st.markdown("<h3>App Settings</h3>", unsafe_allow_html=True)

        st.markdown("<h4>Notifications</h4>", unsafe_allow_html=True)

        email_notifications = st.toggle("Email Notifications", value=True)
        push_notifications = st.toggle("Push Notifications", value=True)

        st.markdown("<h4>Categories</h4>", unsafe_allow_html=True)

        if st.button("Manage Custom Categories"):
            st.info("Feature coming soon!")

        st.markdown("<h4>Data Management</h4>", unsafe_allow_html=True)

        if st.button("Export All Data"):
            # Prepare data for export
            data = {
                "profile": {
                    "full_name": st.session_state.full_name if 'full_name' in st.session_state else "",
                    "email": st.session_state.email if 'email' in st.session_state else "",
                    "subscription": st.session_state.subscription,
                    "balance": st.session_state.balance,
                    "savings": st.session_state.savings,
                    "investments": st.session_state.investments
                },
                "transactions": st.session_state.transactions.to_dict(orient="records") if not st.session_state.transactions.empty else [],
                "goals": st.session_state.goals
            }

            # Convert to JSON
            json_data = json.dumps(data, indent=4)

            # Provide download button
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name="neuro_data_export.json",
                mime="application/json"
            )

        st.markdown("<h4>Danger Zone</h4>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Reset App Data", type="primary"):
                st.warning("This will reset all your data. Are you sure?")
                if st.button("Yes, Reset Everything", key="confirm_reset"):
                    # Reset all session state
                    for key in list(st.session_state.keys()):
                        if key != 'login_status' and key != 'current_page':
                            del st.session_state[key]

                    # Initialize default values
                    st.session_state.subscription = 'Basic'
                    st.session_state.balance = 0.0
                    st.session_state.savings = 0.0
                    st.session_state.investments = 0.0
                    st.session_state.goals = []
                    st.session_state.transactions = pd.DataFrame(columns=["date", "category", "amount", "description", "type"])
                    st.session_state.insights = []
                    st.session_state.roundups = 0.0
                    st.session_state.first_login = True

                    st.success("All data has been reset!")
                    navigate_to("dashboard")
                    st.rerun()

        with col2:
            if st.button("Delete Account", type="primary"):
                st.error("This will permanently delete your account and all data. This action cannot be undone.")
                if st.button("Yes, Delete My Account", key="confirm_delete"):
                    st.session_state.login_status = False
                    st.session_state.current_page = 'login'

                    # Reset all session state
                    for key in list(st.session_state.keys()):
                        if key != 'login_status' and key != 'current_page':
                            del st.session_state[key]

                    st.rerun()

# AI Assistant feature
def display_ai_assistant():
    st.markdown("<h2>AI Financial Assistant</h2>", unsafe_allow_html=True)

    if st.session_state.subscription in ['Pro', 'Elite']:
        st.markdown("""
        <p>Your personal AI financial assistant is here to help. Ask any question about your finances, get advice, or plan for the future.</p>
        """, unsafe_allow_html=True)

        # Quick questions section
        st.markdown("<h3>Quick Questions</h3>", unsafe_allow_html=True)

        quick_questions = [
            "How much did I spend on dining last month?",
            "What's my savings rate?",
            "How can I improve my budget?",
            "Am I on track for my goals?",
            "What's my biggest expense category?"
        ]

        cols = st.columns(len(quick_questions))

        for i, (col, question) in enumerate(zip(cols, quick_questions)):
            with col:
                if st.button(question, key=f"quick_q_{i}"):
                    st.session_state.ai_query = question

        # Chat interface
        if 'ai_messages' not in st.session_state:
            st.session_state.ai_messages = [
                {"role": "assistant", "content": "Hi there! I'm your AI financial assistant. How can I help you today?"}
            ]

        # Display chat messages
        for message in st.session_state.ai_messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input
        if 'ai_query' not in st.session_state:
            st.session_state.ai_query = ""

        user_query = st.chat_input("Ask anything about your finances...", key="chat_input") or st.session_state.ai_query

        if user_query:
            # Reset the stored query
            st.session_state.ai_query = ""

            # Add user message to chat
            st.session_state.ai_messages.append({"role": "user", "content": user_query})

            # Display user message
            with st.chat_message("user"):
                st.write(user_query)

            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    time.sleep(1)  # Simulate AI processing

                    # Sample responses based on query keywords
                    response = "I'm analyzing your financial data..."

                    if "spend" in user_query.lower() and "dining" in user_query.lower():
                        # Calculate dining expenses if we have transaction data
                        if not st.session_state.transactions.empty:
                            # Convert to datetime if needed
                            transactions_df = st.session_state.transactions.copy()
                            if not pd.api.types.is_datetime64_any_dtype(transactions_df['date']):
                                transactions_df['date'] = pd.to_datetime(transactions_df['date'])

                            # Filter for last month and dining category
                            last_month = datetime.now() - timedelta(days=30)
                            mask = (transactions_df['date'] >= last_month) & (transactions_df['category'] == 'Dining')
                            dining_expenses = transactions_df[mask]['amount'].sum()

                            response = f"In the last 30 days, you spent €{abs(dining_expenses):.2f} on dining out. This represents about 15% of your total expenses during this period."
                        else:
                            response = "You don't have any dining transactions recorded yet. Add some transactions so I can analyze your dining expenses."

                    elif "savings rate" in user_query.lower():
                        if not st.session_state.transactions.empty:
                            # Calculate income and expenses
                            transactions_df = st.session_state.transactions.copy()
                            total_income = transactions_df[transactions_df['type'] == 'income']['amount'].sum()
                            total_expenses = abs(transactions_df[transactions_df['type'] == 'expense']['amount'].sum())

                            if total_income > 0:
                                savings_rate = ((total_income - total_expenses) / total_income) * 100
                                response = f"Your overall savings rate is {savings_rate:.1f}%. The recommended savings rate is at least 20%. "

                                if savings_rate < 20:
                                    response += "You might want to look for ways to increase your savings rate."
                                else:
                                    response += "Great job! You're on track with your savings."
                            else:
                                response = "I don't have enough income data to calculate your savings rate yet. Please add your income transactions."
                        else:
                            response = "I don't have enough transaction data to calculate your savings rate yet. Please add some income and expense transactions."

                    elif "improve" in user_query.lower() and "budget" in user_query.lower():
                        response = """Here are some ways to improve your budget:

1. Track all expenses for at least 30 days to understand your spending patterns
2. Use the 50/30/20 rule: 50% for needs, 30% for wants, and 20% for savings
3. Identify and cut unnecessary subscriptions
4. Set specific financial goals to stay motivated
5. Review and adjust your budget monthly"""

                    elif "track" in user_query.lower() and "goals" in user_query.lower():
                        if st.session_state.goals:
                            on_track_goals = []
                            off_track_goals = []

                            for goal in st.session_state.goals:
                                # Calculate expected progress based on time
                                target_date = datetime.strptime(goal["date"], "%Y-%m-%d")
                                start_date = target_date - timedelta(days=365)  # Assume goal was set a year before target
                                total_days = (target_date - start_date).days
                                days_passed = (datetime.now() - start_date).days

                                if total_days > 0 and days_passed > 0:
                                    expected_progress = min(days_passed / total_days, 1) * 100
                                    actual_progress = (goal["current"] / goal["target"]) * 100

                                    if actual_progress >= expected_progress * 0.9:  # Within 90% of expected
                                        on_track_goals.append(goal["name"])
                                    else:
                                        off_track_goals.append(goal["name"])

                            if on_track_goals and off_track_goals:
                                response = f"You're on track with these goals: {', '.join(on_track_goals)}. However, you're falling behind on: {', '.join(off_track_goals)}. Consider adjusting your monthly contributions to catch up."
                            elif on_track_goals:
                                response = f"Great news! You're on track with all your goals: {', '.join(on_track_goals)}. Keep up the good work!"
                            else:
                                response = f"You're currently behind on all your goals: {', '.join(off_track_goals)}. Let's review your budget to find ways to increase your contributions."
                        else:
                            response = "You don't have any financial goals set up yet. Let's set some goals to track your progress!"

                    elif "biggest expense" in user_query.lower():
                        if not st.session_state.transactions.empty:
                            # Filter for expenses
                            transactions_df = st.session_state.transactions.copy()
                            expenses = transactions_df[transactions_df['type'] == 'expense']

                            if not expenses.empty:
                                # Group by category
                                category_expenses = expenses.groupby('category')['amount'].sum().abs()
                                biggest_category = category_expenses.idxmax()
                                biggest_amount = category_expenses.max()

                                response = f"Your biggest expense category is {biggest_category}, where you've spent €{biggest_amount:.2f}. This represents {(biggest_amount / category_expenses.sum() * 100):.1f}% of your total expenses."
                            else:
                                response = "I don't have enough expense data to determine your biggest category. Please add more expense transactions."
                        else:
                            response = "I don't have any transaction data yet. Please add some expense transactions so I can analyze your spending patterns."

                    st.write(response)

                # Add AI response to chat history
                st.session_state.ai_messages.append({"role": "assistant", "content": response})
    else:
        st.warning("The AI Financial Assistant is available with Pro and Elite subscriptions.")
        if st.button("Upgrade Subscription"):
            navigate_to("subscription")
            st.rerun()

# Main application
def main():
    # Initialize session state variables if they don't exist
    if 'login_status' not in st.session_state:
        st.session_state.login_status = False

    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login'

    # Apply custom styling
    apply_custom_styles()

    # Display header
    display_header()

    # Check login status
    if not st.session_state.login_status:
        display_login()
    else:
        # Display sidebar navigation
        display_sidebar()

        # Display current page content
        if st.session_state.current_page == 'dashboard':
            display_dashboard()
        elif st.session_state.current_page == 'transactions':
            display_transactions()
        elif st.session_state.current_page == 'goals':
            display_goals()
        elif st.session_state.current_page == 'subscription':
            display_subscription()
        elif st.session_state.current_page == 'profile':
            display_profile()
        elif st.session_state.current_page == 'ai_assistant':
            display_ai_assistant()
        else:
            display_dashboard()  # Default to dashboard

# Initialize session state for user data entry
def initialize_session_state():
    # App settings
    if 'subscription' not in st.session_state:
        st.session_state.subscription = 'Basic'

    # User financial data
    if 'balance' not in st.session_state:
        st.session_state.balance = 0.0
    if 'savings' not in st.session_state:
        st.session_state.savings = 0.0
    if 'investments' not in st.session_state:
        st.session_state.investments = 0.0

    # Transactions
    if 'transactions' not in st.session_state:
        st.session_state.transactions = pd.DataFrame(columns=["date", "category", "amount", "description", "type"])

    # Goals
    if 'goals' not in st.session_state:
        st.session_state.goals = []

    # Insights
    if 'insights' not in st.session_state:
        st.session_state.insights = []

    # Roundups
    if 'roundups' not in st.session_state:
        st.session_state.roundups = 0.0

    # First login flag
    if 'first_login' not in st.session_state:
        st.session_state.first_login = True

# Custom styles
def apply_custom_styles():
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            padding: 1rem 0;
            background-color: #f8f9fa;
            border-radius: 10px;
            margin-bottom: 1rem;
        }

        .balance-card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            margin-bottom: 1rem;
        }

        .insights-card {
            background-color: #f0f4f8;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
        }

        .subscription-card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            height: 100%;
            position: relative;
        }

        .basic-card {
            border-top: 4px solid #6c757d;
        }

        .pro-card {
            border-top: 4px solid #007bff;
        }

        .elite-card {
            border-top: 4px solid #17a2b8;
        }

        .progress-container {
            width: 100%;
            background-color: #e9ecef;
            border-radius: 5px;
            height: 10px;
            overflow: hidden;
        }

        .progress-bar {
            height: 100%;
            border-radius: 5px;
        }

        /* Custom sidebar */
        .css-1d391kg {
            background-color: #f8f9fa;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Login form styling */
        .login-form {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

# App header
def display_header():
    st.markdown("""
    <div class="main-header">
        <h1>Neuro Finance</h1>
        <p>Your intelligent financial assistant</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar navigation
def display_sidebar():
    with st.sidebar:
        st.markdown("## Navigation")

        if st.button("Dashboard", use_container_width=True):
            navigate_to("dashboard")
            st.rerun()

        if st.button("Transactions", use_container_width=True):
            navigate_to("transactions")
            st.rerun()

        if st.button("Financial Goals", use_container_width=True):
            navigate_to("goals")
            st.rerun()

        if st.button("AI Assistant", use_container_width=True):
            navigate_to("ai_assistant")
            st.rerun()

        if st.button("Subscription", use_container_width=True):
            navigate_to("subscription")
            st.rerun()

        if st.button("Profile & Settings", use_container_width=True):
            navigate_to("profile")
            st.rerun()

        st.markdown("---")

        # Show current subscription
        st.markdown(f"Current Plan: **{st.session_state.subscription}**")

        # Logout button
        if st.button("Logout", use_container_width=True):
            st.session_state.login_status = False
            st.session_state.current_page = 'login'
            st.rerun()

# Login page
def display_login():
    st.markdown("""
    <div class="login-form">
        <h2 style="text-align: center;">Welcome to Neuro Finance</h2>
        <p style="text-align: center;">Your intelligent financial assistant</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        with st.form("login_form"):
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")

            if login_button:
                # For demo purposes, any non-empty username/password works
                if username and password:
                    st.session_state.login_status = True
                    st.session_state.current_page = 'dashboard'
                    initialize_session_state()
                    st.rerun()
                else:
                    st.error("Please enter username and password")

    with col2:
        with st.form("register_form"):
            st.subheader("Register")
            new_username = st.text_input("Choose Username")
            new_password = st.text_input("Choose Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            register_button = st.form_submit_button("Register")

            if register_button:
                if new_username and new_password and new_password == confirm_password:
                    st.session_state.login_status = True
                    st.session_state.current_page = 'dashboard'
                    initialize_session_state()
                    st.rerun()
                elif not new_username or not new_password:
                    st.error("Please fill in all fields")
                else:
                    st.error("Passwords do not match")

# Run the app
if __name__ == "__main__":
    try:
        import pandas as pd
        import json
        from datetime import datetime, timedelta

        # Initialize session state variables on first run
        initialize_session_state()

        # Run the main app
        main()
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Please make sure you have the required libraries installed: pandas, json")

           
