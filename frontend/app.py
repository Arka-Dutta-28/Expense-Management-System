import streamlit as st
from add_update import add_update_tab
from retrieve_day import retrieve_day_tab
from retrieve_month import retrieve_month_tab
from retrieve_all import retrieve_all_tab
from analytics_by_category import analytics_category_tab
from analytics_by_months import analytics_months_tab


st.title("Expense Tracking System")

tab1, tab2, tab3 = st.tabs(["Retrieve", "Add/Update", "Analytics"])

with tab1:
    tab11, tab12, tab13 = st.tabs(["Recent", "By Date", "By Month"])
    with tab11:
        retrieve_all_tab()
    with tab12:
        retrieve_day_tab()
    with tab13:
        retrieve_month_tab()

with tab2:
    add_update_tab()

with tab3:
    tab31, tab32 = st.tabs(["By Category", "By Months"])
    with tab31:
        analytics_category_tab()
    with tab32:
        analytics_months_tab()