import streamlit as st
import requests
import pandas as pd
import altair as alt
from datetime import date
import calendar

API_URL = "http://localhost:8000"

def retrieve_month_tab():
    st.subheader("Monthly Expenses Viewer")

    selected_date = st.date_input("Select any date in the month you want to retrieve:", value=date.today())
    selected_year = selected_date.year
    selected_month = selected_date.month

    if st.button("Retrieve Data"):
        response = requests.get(
            f"{API_URL}/expenses_month/",
            params={"year": selected_year, "month": selected_month}
        )

        if response.status_code == 404:
            st.error("Data Not found")
            return
        elif response.status_code != 200:
            st.error("Failed to retrieve expenses")
            return

        data = response.json()
        df = pd.DataFrame(data)

        if df.empty:
            st.warning("No expenses found for the selected month.")
            return


        df.index += 1
        df.columns = df.columns.str.capitalize()

        total = df["Amount"].sum()
        st.write(f"Total Expenditure for the month of {calendar.month_name[selected_month]} is {total:.2f}")

        df_month = df.copy()
        df_month["Amount"] = df_month["Amount"].map("{:.2f}".format)
        st.table(df_month)



        st.subheader("Visualization By Category")

        df_table = (
            df.groupby("Category", as_index=False)["Amount"]
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

        st.subheader("Sorted by Amount")
        st.table(df_table)
