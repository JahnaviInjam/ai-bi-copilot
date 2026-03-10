from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from generate_sql import generate_sql, run_sql

app = FastAPI(title="AI BI Copilot API")

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "AI BI Copilot API is running"}

@app.post("/ask")
def ask_question(payload: QuestionRequest):
    try:
        sql = generate_sql(payload.question)
        df = run_sql(sql)

        return {
            "question": payload.question,
            "sql": sql,
            "rows": df.to_dict(orient="records"),
            "columns": list(df.columns),
        }
    except Exception as e:
        import traceback
        raise HTTPException(status_code=400, detail=traceback.format_exc())