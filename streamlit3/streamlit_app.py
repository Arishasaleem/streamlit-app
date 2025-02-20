import streamlit as st
import pandas as pd
import plotly.express as px
import os

# CSV File for storing expenses
CSV_FILE = "expenses.csv"

# Function to load existing data
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Date", "Category", "Amount"])

# Function to save data
def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# Streamlit UI
st.title("💰 Expense Tracker")

# Expense Input Form
st.sidebar.header("Add New Expense")
date = st.sidebar.date_input("Date")
category = st.sidebar.selectbox("Category", ["Food", "Transport", "Shopping", "Rent", "Other"])
amount = st.sidebar.number_input("Amount (in USD)", min_value=0.01, step=0.01, format="%.2f")

if st.sidebar.button("Add Expense"):
    df = load_data()
    new_entry = pd.DataFrame({"Date": [date], "Category": [category], "Amount": [amount]})
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)
    st.sidebar.success("Expense Added Successfully!")

# Load Expenses
df = load_data()
st.subheader("📋 Expense List")
st.dataframe(df)

# Delete Last Entry Button
if not df.empty and st.button("Delete Last Entry"):
    df = df[:-1]  # Remove last row
    save_data(df)
    st.warning("Last entry deleted!")

# Summary & Visualization
st.subheader("📊 Expense Summary")
if not df.empty:
    summary = df.groupby("Category")["Amount"].sum().reset_index()
    fig = px.bar(summary, x="Category", y="Amount", title="Category-wise Expense Breakdown", text_auto=True)
    st.plotly_chart(fig)
else:
    st.info("No expenses added yet.")
