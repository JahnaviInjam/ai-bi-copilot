import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import plotly.express as px

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SCHEMA = """
Table: sales

Columns:
order_id
order_date
region
product_name
category
quantity
unit_price
total_sales
"""

SYSTEM_PROMPT = f"""
You convert natural language questions into SQL queries.

Database type: SQLite

{SCHEMA}

Rules:
- Return only SQL
- Only SELECT queries
- Use only the columns listed above
- Do not invent tables or columns
- Use valid SQLite syntax
- When using aggregations like SUM, AVG, or COUNT, include the aggregated metric in the SELECT output
- When answering ranking questions like top, highest, most, best, lowest, return both the entity and the metric
- Do not include markdown
- Do not include explanations

Examples:

Question: show total sales by region
SQL:
SELECT region, SUM(total_sales) AS total_sales
FROM sales
GROUP BY region;

Question: show top 5 products by total sales
SQL:
SELECT product_name, SUM(total_sales) AS total_sales
FROM sales
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 5;

Question: which category generates the most revenue
SQL:
SELECT category, SUM(total_sales) AS total_revenue
FROM sales
GROUP BY category
ORDER BY total_revenue DESC
LIMIT 1;

Question: show average unit price by category
SQL:
SELECT category, AVG(unit_price) AS avg_unit_price
FROM sales
GROUP BY category;
"""

def clean_sql(sql: str) -> str:
    sql = sql.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

def validate_sql(sql: str) -> None:
    sql_upper = sql.upper().strip()

    forbidden_keywords = [
        "DROP", "DELETE", "UPDATE", "INSERT",
        "ALTER", "TRUNCATE", "CREATE", "REPLACE"
    ]

    if not sql_upper.startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed.")

    for keyword in forbidden_keywords:
        if keyword in sql_upper:
            raise ValueError(f"Forbidden SQL keyword detected: {keyword}")
        
def generate_sql(question):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()

    sql = response.choices[0].message.content
    sql = clean_sql(sql)
    return sql


def run_sql(sql_query):
    validate_sql(sql_query)

    conn = sqlite3.connect("data/sales.db")

    df = pd.read_sql(sql_query, conn)

    conn.close()

    return df


def create_chart(df):

    if len(df.columns) == 2:

        x = df.columns[0]
        y = df.columns[1]

        fig = px.bar(df, x=x, y=y, title=f"{y} by {x}")

        fig.show()

if __name__ == "__main__":

    question = input("Ask your question: ")

    sql = generate_sql(question)

    print("\nGenerated SQL:\n")
    print(sql)

    print("\nQuery Result:\n")

    result = run_sql(sql)

    print(result)

    create_chart(result)


