from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Snowflake RAG Assistant",
    description="Enterprise RAG over Snowflake documentation",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"status": "ok", "message": "RAG API is running"}


app.include_router(router)
