# ==========================================
# main.py
# ==========================================
from fastapi import FastAPI
from pydantic import BaseModel
from Backend.agents.digging_agent import info_company
from fastapi.responses import PlainTextResponse
app = FastAPI()

class CompanyRequest(BaseModel):
    name: str

@app.post("/info")
def get_info(payload: CompanyRequest):
    result = info_company(payload.name)
    return {"report": result}