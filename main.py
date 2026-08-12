from fastapi import FastAPI 
from Backend.agents.cold_mail_agent import get_cold_email

app=FastAPI()
@app.get("/")
def get_data():
    return get_cold_email()