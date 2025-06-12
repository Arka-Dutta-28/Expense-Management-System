import streamlit as st
import requests
import pandas as pd
import altair as alt

API_URL = "http://localhost:8000"

def retrieve_day_tab():
    st.subheader("Daily Expense Viewer")

    # Step 1: User selects date
    selected_date = st.date_input("Enter date to retrieve expenses:")

    # Step 2: User selects view type
    view_option = st.radio("Select View", ["Retrieve Data", "Visualization by Category"], horizontal=True)

    # Step 3: Button to trigger API call
    if st.button("Get Expenses"):
        # API call
        response = requests.get(f"{API_URL}/expenses/{selected_date}")

        if response.status_code != 200:
            st.error("Failed to retrieve expenses")
            return

        data = response.json()
        df = pd.DataFrame(data)

        if df.empty:
            st.warning("No expenses found for selected date.")
            return

        # Sort and format
        df_sorted = df.sort_values(by="amount", ascending=False).reset_index(drop=True)
        df_sorted.index += 1
        df_sorted.columns = df_sorted.columns.str.capitalize()

        # Display table or chart based on selection
        if view_option == "Retrieve Data":
            st.write(f"The total expenditure on {selected_date} is {df_sorted.Amount.sum():.2f}")
            df_sorted.set_index("Category",inplace=True)
            st.write(df_sorted)

        elif view_option == "Visualization by Category":
            df_table = (
                df_sorted.groupby("Category", as_index=False)["Amount"]
                .sum()
                .sort_values(by="Amount", ascending=False)
            )

            total = df_table["Amount"].sum()
            df_table["Percentage"] = (df_table["Amount"] / total * 100).round(2)

            chart = alt.Chart(df_table).mark_bar().encode(
                x=alt.X("Category:N", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Percentage:Q"),
                tooltip=["Category", "Amount", "Percentage"]
            ).properties(
                width="container",
                height=400
            )

            st.altair_chart(chart, use_container_width=True)

            df_table.set_index("Category", inplace=True)
            df_table["Amount"] = df_table["Amount"].map("{:.2f}".format)
            df_table["Percentage"] = df_table["Percentage"].map("{:.2f}".format)

            st.table(df_table)