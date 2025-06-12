import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def retrieve_all_tab():
    last_expenses = st.number_input(label="How many recent expenses would you like to see?",min_value=1, max_value=10000,
                                   value=10, step=1, key="last_expenses",label_visibility="collapsed")

    if st.button("Get Data"):

        response = requests.get(f"{API_URL}/recent_expenses/{last_expenses}")

        if response.status_code != 200:
            st.error("Failed to retrieve expenses")
            return

        data = response.json()
        df = pd.DataFrame(data)

        if df.empty:
            st.warning("No expenses is added yet.")
            return

        df.index += 1
        df.columns = df.columns.str.capitalize()

        df["Amount"] = df["Amount"].map("{:.2f}".format)

        st.subheader("📒 Expense Passbook")
        st.table(df)
        st.write(f"The total expenditure for the last {len(df)} expenses is {df.Amount.astype(float).sum():.2f}")