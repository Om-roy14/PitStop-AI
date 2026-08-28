from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from Backend.Databases.database import Base

# =========================================
# USER
# =========================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False) # Stores the hashed password
    linkedin_id = Column(String(150), nullable=True) 
    github_id = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships to isolated data
    portfolios = relationship("Portfolio", back_populates="owner")
    emails = relationship("EmailLog", back_populates="owner")
    researches = relationship("CompanyResearch", back_populates="owner")


# =========================================
# PORTFOLIO
# =========================================
class Portfolio(Base):
    __tablename__ = "portfolio"

    Project_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False) # THE ISOLATION LINK
    Project_name = Column(String(100), nullable=False)
    teck_stack = Column(Text, nullable=False)  # Allows for longer text than String
    github_repo = Column(String(255), nullable=True)
    
    owner = relationship("User", back_populates="portfolios")


# =========================================
# EMAIL LOGS & RESEARCH
# =========================================
class EmailLog(Base):
    __tablename__ = "email_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    company_url = Column(String(255), nullable=False)
    recipient_email = Column(String(150), nullable=True)
    email_content = Column(Text, nullable=False)
    status = Column(String(50), default="generated") # 'generated', 'sent', 'failed'
    error_message = Column(Text, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="emails")


class CompanyResearch(Base):
    __tablename__ = "company_research"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    company_name = Column(String(150), nullable=False)
    report = Column(Text, nullable=False)
    searched_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="researches")