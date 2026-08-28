from typing import Optional
from sqlalchemy.orm import Session

from Backend.Databases.models import Portfolio

# =========================================
# CREATE PORTFOLIO
# =========================================
def add_portfolio(
    db: Session,
    user_id: int,
    project_name: str,
    teck_stack: str,
    github_repo: str
):
    new_portfolio = Portfolio(
        user_id=user_id,
        Project_name=project_name,
        teck_stack=teck_stack,
        github_repo=github_repo
    )
    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)
    return new_portfolio


# =========================================
# READ PORTFOLIOS
# =========================================
# Fetch all portfolio items with pagination
def get_all_portfolios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Portfolio).offset(skip).limit(limit).all()


# Fetch a single portfolio item by its ID
def get_portfolio_by_id(db: Session, project_id: int):
    return db.query(Portfolio).filter(Portfolio.Project_id == project_id).first()
  

# =========================================
# UPDATE PORTFOLIO
# =========================================
def update_portfolio(
    db: Session,
    project_id: int,
    project_name: Optional[str] = None,
    teck_stack: Optional[str] = None,
    github_repo: Optional[str] = None,
):
    portfolio = db.query(Portfolio).filter(Portfolio.Project_id == project_id).first()

    if not portfolio:
        return None

    if project_name is not None:
        portfolio.Project_name = project_name
    if teck_stack is not None:
        portfolio.teck_stack = teck_stack
    if github_repo is not None:
        portfolio.github_repo = github_repo

    db.commit()
    db.refresh(portfolio)
    return portfolio


# =========================================
# DELETE PORTFOLIO
# =========================================
def delete_portfolio(db: Session, project_id: int):
    portfolio = db.query(Portfolio).filter(Portfolio.Project_id == project_id).first()

    if not portfolio:
        return None

    db.delete(portfolio)
    db.commit()
    return portfolio