import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="AI Business Intelligence Copilot", layout="wide")

st.title("AI Business Intelligence Copilot")
st.markdown("""
Example questions:
- Show total sales by region
- Show top 5 products by total sales
- Which category generates the most revenue
- Show sales by category
""")
st.write("Ask a business question about the sales data.")

with st.form("query_form"):
    question = st.text_input(
        "Ask a business question",
        placeholder="e.g. show total sales by region"
    )
    submit = st.form_submit_button("Generate Insights")

if submit and question:

    with st.spinner("Generating insights..."):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={"question": question},
                timeout=60
            )

            response.raise_for_status()
            if response.status_code != 200:
                st.error(response.text)
                st.stop()

            result = response.json()

            st.subheader("Generated SQL")
            st.code(result["sql"], language="sql")

            df = pd.DataFrame(result["rows"])

            left_col, right_col = st.columns(2)

            with left_col:
                st.subheader("Query Result")
                st.dataframe(df, use_container_width=True)

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
                    st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")