import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import  altair as alt

API_URL = "http://localhost:8000"


def analytics_category_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.today().replace(day=1))

    with col2:
        end_date = st.date_input("End Date", min_value=start_date)

    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        response = requests.post(f"{API_URL}/analytics/", json=payload)
        response = response.json()

        data = {
            "Category": list(response.keys()),
            "Total": [response[category]["total"] for category in response],
            "Percentage": [response[category]["percentage"] for category in response]
        }

        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by="Percentage", ascending=False)

        st.write(f"The total expenditure from {start_date} to {end_date} is {df_sorted.Total.sum():.2f}")

        df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
        df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)

        st.subheader("Expense Breakdown By Category")

        # st.bar_chart(data=df_sorted.set_index("Category")['Percentage'], width=0, height=0, use_container_width=True)
        chart_category = alt.Chart(df_sorted).mark_bar().encode(
            x=alt.X("Category:N", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Percentage:Q"),
            tooltip=["Category", "Total", "Percentage"]
        ).properties(
            width="container",
            height=400
        )

        st.altair_chart(chart_category, use_container_width=True)

        st.table(df_sorted.set_index("Category"))