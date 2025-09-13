import streamlit as st
import requests
import pandas as pd
import calendar

API_URL = "http://localhost:8000"

def analytics_month_tab():
    if st.button("Get Analytics by Month"):
        response = requests.get(f"{API_URL}/analytics_month/")
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            df = df.rename(columns={
                "expense_month": "Month",
                "total_expense": "Expenses"
            })

            df["Month_Num"] = df["Month"].apply(lambda x: list(calendar.month_name).index(x))


            df_sorted = df.sort_values("Month_Num").drop(columns="Month_Num")
            st.subheader("Graphical Representation:")
            st.bar_chart(df_sorted.set_index('Month')['Expenses'],width=0,height=0,use_container_width=True)
            df_sorted["Expenses"] = df_sorted["Expenses"].map("{:,.2f}".format)
            st.subheader("Tabular Representation:")
            st.table(df_sorted)
        else:
            st.error("Failed to retrieve expenses")
            data = []

