import os
from datetime import datetime
from typing import List, Optional

from dotenv import load_dotenv
load_dotenv()

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

# ==========================================
# BACKEND IMPORTS
# ==========================================
from Backend.agents.cold_mail_agent import get_cold_email
from Backend.agents.digging_agent import info_company
from Backend.email_service import send_real_email
from Backend.auth import login_user, register_user, create_access_token, get_current_user
from Backend.Databases.database import Base, engine, get_db
from Backend.Databases.models import User, Portfolio, EmailLog, CompanyResearch

# ==========================================
# APP SETUP
# ==========================================
app = FastAPI(title="PitStop AI API")

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Enable CORS so your Vercel frontend can talk to this Railway backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# REQUEST MODELS
# ==========================================
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    linkedin_id: Optional[str] = None
    github_id: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class PortfolioRequest(BaseModel):
    project_name: str
    tech_stack: str
    github_repo: Optional[str] = None

class EmailRequest(BaseModel):
    url: str
    name: Optional[str] = None

class EmailSendRequest(BaseModel):
    log_id: int
    recipient_email: str

class CompanyRequest(BaseModel):
    name: str

# ==========================================
# API: AUTHENTICATION
# ==========================================
@app.post("/api/signup")
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(
        db=db, name=user_data.name, email=user_data.email,
        password=user_data.password, linkedin_id=user_data.linkedin_id, github_id=user_data.github_id
    )
    if user is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"message": "Registration successful"}

@app.post("/api/login")
def login(user_data: LoginRequest, db: Session = Depends(get_db)):
    user = login_user(db=db, email=user_data.email, password=user_data.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"name": user.name, "email": user.email}
    }

# ==========================================
# API: DASHBOARD STATS
# ==========================================
@app.get("/api/dashboard/stats")
def get_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    emails_sent = db.query(EmailLog).filter(EmailLog.user_id == current_user.id, EmailLog.status == "sent").count()
    companies_checked = db.query(CompanyResearch).filter(CompanyResearch.user_id == current_user.id).count()
    return {
        "total_emails_sent": emails_sent,
        "total_companies_checked": companies_checked,
        "user_name": current_user.name
    }

# ==========================================
# API: PORTFOLIO
# ==========================================
@app.get("/api/portfolio")
def read_all_portfolios(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    portfolios = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).all()
    return [
        {"id": p.Project_id, "project_name": p.Project_name, "tech_stack": p.teck_stack, "github_repo": p.github_repo} 
        for p in portfolios
    ]

@app.post("/api/portfolio", status_code=status.HTTP_201_CREATED)
def add_project(portfolio_data: PortfolioRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_port = Portfolio(
        user_id=current_user.id,
        Project_name=portfolio_data.project_name,
        teck_stack=portfolio_data.tech_stack,
        github_repo=portfolio_data.github_repo
    )
    db.add(new_port)
    db.commit()
    db.refresh(new_port)
    return {"message": "Portfolio added successfully"}

@app.delete("/api/portfolio/{project_id}")
def remove_portfolio(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Portfolio).filter(Portfolio.Project_id == project_id, Portfolio.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not owned by you.")
    db.delete(project)
    db.commit()
    return {"message": "Deleted successfully"}

# ==========================================
# API: COLD EMAIL GENERATE & SEND
# ==========================================
@app.post("/api/email/generate")
def generate_email(request: EmailRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        content = get_cold_email(url=request.url, name=current_user.name)
        log = EmailLog(user_id=current_user.id, company_url=request.url, email_content=content, status="generated")
        db.add(log)
        db.commit()
        db.refresh(log)
        return {"log_id": log.id, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/email/send")
def send_email(req: EmailSendRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    log = db.query(EmailLog).filter(EmailLog.id == req.log_id, EmailLog.user_id == current_user.id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Email record not found")
    
    subject = f"Connecting regarding {log.company_url}"
    success, error = send_real_email(req.recipient_email, subject, log.email_content)
    
    if success:
        log.status = "sent"
        log.recipient_email = req.recipient_email
        log.sent_at = datetime.utcnow()
        db.commit()
        return {"message": "Email sent"}
    else:
        log.status = "failed"
        log.error_message = error
        db.commit()
        raise HTTPException(status_code=500, detail=f"SMTP Error: {error}")

# ==========================================
# API: COMPANY RESEARCH
# ==========================================
@app.post("/info")
def get_info(payload: CompanyRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        result = info_company(payload.name)
        research = CompanyResearch(user_id=current_user.id, company_name=payload.name, report=result)
        db.add(research)
        db.commit()
        return {"report": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))