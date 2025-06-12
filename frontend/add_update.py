import streamlit as st
import requests

API_URL = "http://localhost:8000"

def add_update_tab():
    selected_date = st.date_input("Enter date to add or update expenses:")

    if st.button("Add/Update Expenses"):
        response = requests.get(f"{API_URL}/expenses/{selected_date}")
        if response.status_code == 200:
            existing_expenses = response.json()
        else:
            st.error("Failed to retrieve expenses")
            existing_expenses = []

        categories = ["Rent", "Food", "Education", "Shopping", "Entertainment", "Travel", "Other"]

        st.markdown(f"##### Total entries for {selected_date}: {len(existing_expenses)}", unsafe_allow_html=True)

        default_count = len(existing_expenses) if existing_expenses else 1
        num_expenses = st.number_input("To add an expense, use '+'", min_value=1, max_value=20,
                                       value=default_count, step=1, key="num_expenses")

        with st.form(key="expense_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.text("Amount")
            with col2:
                st.text("Category")
            with col3:
                st.text("Notes")

            expenses = []
            for i in range(num_expenses):
                if i < len(existing_expenses):
                    amount = existing_expenses[i].get('amount', 0.0)
                    category = existing_expenses[i].get("category", "Shopping")
                    notes = existing_expenses[i].get("notes", "")
                else:
                    amount = 0.0
                    category = "Shopping"
                    notes = ""

                col1, col2, col3 = st.columns(3)
                with col1:
                    amount_input = st.number_input("Amount", min_value=0.0, step=1.0, value=amount,
                                                   key=f"{selected_date}amount_{i}", label_visibility="collapsed")
                with col2:
                    category_input = st.selectbox("Category", options=categories,
                                                  index=categories.index(category),
                                                  key=f"{selected_date}category_{i}", label_visibility="collapsed")
                with col3:
                    notes_input = st.text_input("Notes", value=notes,
                                                key=f"{selected_date}notes_{i}", label_visibility="collapsed")

                expenses.append({
                    'amount': amount_input,
                    'category': category_input,
                    'notes': notes_input
                })

            submit_button = st.form_submit_button("Save Expenses")
            if submit_button:
                filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]
                response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
                if response.status_code == 200:
                    st.success("Expenses updated successfully!")
                else:
                    st.error("Failed to update expenses.")

        st.info(
            "To delete an expense on a certain date, simply set its **amount to 0** and click **Save Expenses**.  \n"
            "The system will treat it as a deletion."
        )