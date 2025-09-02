import streamlit as st
from utils.expenseTracker import Account
import time

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to see your expenses")
    st.stop()

user_email = st.session_state.user_email
db_name = f"{user_email}.db"

account = Account(db_name = db_name)
st.title("💳 Your Transactions")
st.divider()


#Expense section
st.subheader("View Expense 🧾")
expenses_df = account.expenseList()

if expenses_df.empty:
    st.caption("No Expenses to show ⛔")

else:
    st.dataframe(expenses_df)

if not expenses_df.empty:
    with st.expander("Delete Expense"):
        with st.form("delete expense form"):
            expense_id = st.number_input("Expense Id to Delete",min_value=0,step = 1)
            if st.form_submit_button("🗑️ Delete"):
                account.deleteExpense(expense_id)
                st.toast("✅ Expense Deleted Successfully!")
                time.sleep(1.5)
                st.rerun()


#income section
st.subheader("View Income")
income_df = account.incomeList()

if income_df.empty:
    st.caption("No Income to show ⛔")

else:
    st.dataframe(income_df)

#Delete Income
if not income_df.empty:
    with st.expander("Delete Income"):
        with st.form("delete income form"):
            income_id = st.number_input("Expense Id to Delete",min_value=0,step=1)
            if st.form_submit_button("🗑️ Delete"):
                account.deleteIncome(income_id)
                st.toast("✅ Income Deleted Successfully!")
                time.sleep(1.5)
                st.rerun()

                