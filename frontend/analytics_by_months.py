import streamlit as st
import requests
import pandas as pd
import altair as alt


API_URL = "http://localhost:8000"


def analytics_months_tab():
    response = requests.get(f"{API_URL}/monthly_summary/")
    monthly_summary = response.json()

    df = pd.DataFrame(monthly_summary)
    df.rename(columns={
        "expense_month": "Month Number",
        "month_name": "Month Name",
        "total": "Total"
    }, inplace=True)
    df_sorted = df.sort_values(by="Month Number").reset_index(drop=True)

    df_sorted["Percentage"] = df_sorted["Total"] * 100 / df_sorted.Total.sum()

    st.write(f"The total expenditure up to now is {df_sorted.Total.sum():.2f}")
    df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
    df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)

    st.subheader("Expense Breakdown By Months")

    month_order = df_sorted["Month Name"].tolist()
    chart_month = alt.Chart(df_sorted).mark_bar().encode(
        x=alt.X("Month Name:N", sort=month_order, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Total:Q"),
        tooltip=["Month Name", "Total", "Percentage"]
    ).properties(
        width="container",
        height=400
    )

    st.altair_chart(chart_month, use_container_width=True)

    df_sorted.set_index("Month Name", inplace=True)

    st.table(df_sorted[["Total", "Percentage"]])