import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

from generate_sql import generate_sql

st.set_page_config(page_title="AI Business Intelligence Copilot", layout="wide")

st.title("AI Business Intelligence Copilot")

st.markdown("""
Example questions:

- Show total sales by region
- Show top 5 products by total sales
- Which category generates the most revenue
- Show sales by category
""")

with st.form("query_form"):
    question = st.text_input(
        "Ask a business question",
        placeholder="e.g. show total sales by region"
    )
    submit = st.form_submit_button("Generate Insights")

if submit and question:
    with st.spinner("Generating insights..."):
        try:
            sql = generate_sql(question)

            st.subheader("Generated SQL")
            st.code(sql, language="sql")

            conn = sqlite3.connect("data/sales.db")
            df = pd.read_sql(sql, conn)
            conn.close()

            left_col, right_col = st.columns(2)

            with left_col:
                st.subheader("Query Result")
                st.dataframe(df, width="stretch")

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download results as CSV",
                    csv,
                    "query_results.csv",
                    "text/csv"
                )

            with right_col:
                if len(df.columns) == 2:
                    x = df.columns[0]
                    y = df.columns[1]
                    fig = px.bar(df, x=x, y=y, title=f"{y} by {x}")
                    st.plotly_chart(fig, width="stretch")
                else:
                    st.info("Chart preview is available for 2-column query results.")

        except Exception as e:
            st.error(f"Error: {e}")