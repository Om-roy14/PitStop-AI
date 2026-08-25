from typing import List, Optional
from Backend.functions.portfolio_acccess import (
    add_portfolio,
    delete_portfolio,
    get_all_portfolios,
    get_portfolio_by_id,
    update_portfolio,
)
from Backend.agents.cold_mail_agent import get_cold_email
from Backend.auth import (
    login_user,
    register_user,
)
from Backend.Databases.database import Base, engine, get_db
# Added 'Header' to imports for token checking
from fastapi import Depends, FastAPI, HTTPException, status, Header
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from pathlib import Path

# =========================================
# APP & DATABASE
# =========================================

app = FastAPI(title="PitStop AI")

Base.metadata.create_all(bind=engine)

# =========================================
# FRONTEND
# =========================================
STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Mount FRONTEND folder if you want script.js accessible via /frontend/...
app.mount("/frontend", StaticFiles(directory="FRONTEND"), name="frontend")

# --- HTML PAGE ROUTES ---

@app.get("/")
def serve_landing_page():
    return FileResponse("FRONTEND/landing_page.html")

@app.get("/login")
def serve_login_page():
    return FileResponse("FRONTEND/login.html")

@app.get("/signup")
def serve_signup_page():
    return FileResponse("FRONTEND/signup.html")

@app.get("/dashboard")
def serve_dashboard_page():
    return FileResponse("FRONTEND/dashboard.html")

@app.get("/portfolio_store")
def serve_portfolio_ui():
    return FileResponse("FRONTEND/db.html")

@app.get("/generator")
def serve_generator_page():
    return FileResponse("FRONTEND/index2.html")

# =========================================
# REQUEST & RESPONSE MODELS
# =========================================

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    linkedin_id: str
    github_id: str

class LoginRequest(BaseModel):
    email: str
    password: str

class PortfolioRequest(BaseModel):
    Project_id: int
    Project_name: str
    teck_stack: str
    github_repo: str

class PortfolioUpdateRequest(BaseModel):
    Project_name: Optional[str] = None
    teck_stack: Optional[str] = None
    github_repo: Optional[str] = None

class PortfolioResponse(BaseModel):
    Project_id: int
    Project_name: str
    teck_stack: str
    github_repo: str
    model_config = ConfigDict(from_attributes=True)

class EmailRequest(BaseModel):
    url: str
    name: str

# =========================================
# SECURITY DEPENDENCY
# =========================================
def get_current_user(authorization: str = Header(default=None)):
    """
    Security Gate: Checks if the frontend sent a valid token.
    If no token is provided, it blocks the API request.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Please log in.",
        )
    # In a production app, you would decode a real JWT here.
    # For now, we just ensure a token was provided.
    return authorization


# =========================================
# REGISTER & LOGIN
# =========================================

@app.post("/register")
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(
        db=db,
        name=user_data.name,
        email=user_data.email,
        password=user_data.password,
        linkedin_id=user_data.linkedin_id,
        github_id=user_data.github_id,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    return {
        "message": "Registration successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "linkedin_id": user.linkedin_id,
            "github_id": user.github_id,
        },
    }

@app.post("/login")
def login(user_data: LoginRequest, db: Session = Depends(get_db)):
    user = login_user(db=db, email=user_data.email, password=user_data.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return {
        "message": "Login successful",
        "token": f"mock-jwt-token-for-{user.email}", # Gives the frontend a token to store
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "linkedin_id": user.linkedin_id,
            "github_id": user.github_id,
        },
    }


# =========================================
# PORTFOLIO CRUD (SECURED)
# =========================================

@app.post("/portfolio", status_code=status.HTTP_201_CREATED)
def add_project(
    portfolio_data: PortfolioRequest, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user) # Security lock
):
    existing = get_portfolio_by_id(db=db, project_id=portfolio_data.Project_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project with ID {portfolio_data.Project_id} already exists",
        )

    port = add_portfolio(
        db=db,
        project_id=portfolio_data.Project_id,
        project_name=portfolio_data.Project_name,
        teck_stack=portfolio_data.teck_stack,
        github_repo=portfolio_data.github_repo,
    )

    return {
        "message": "Portfolio added successfully",
        "portfolio": {
            "Project_id": port.Project_id,
            "Project_name": port.Project_name,
            "teck_stack": port.teck_stack,
            "github_repo": port.github_repo,
        },
    }


@app.get("/portfolio", response_model=List[PortfolioResponse])
def read_all_portfolios(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user) # Security lock
):
    return get_all_portfolios(db=db, skip=skip, limit=limit)


@app.get("/portfolio/{project_id}", response_model=PortfolioResponse)
def read_single_portfolio(
    project_id: int, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user) # Security lock
):
    project = get_portfolio_by_id(db=db, project_id=project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found",
        )
    return project


@app.put("/portfolio/{project_id}")
def edit_portfolio(
    project_id: int,
    portfolio_data: PortfolioUpdateRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user) # Security lock
):
    updated_project = update_portfolio(
        db=db,
        project_id=project_id,
        project_name=portfolio_data.Project_name,
        teck_stack=portfolio_data.teck_stack,
        github_repo=portfolio_data.github_repo,
    )

    if updated_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found",
        )

    return {
        "message": "Portfolio updated successfully",
        "portfolio": {
            "Project_id": updated_project.Project_id,
            "Project_name": updated_project.Project_name,
            "teck_stack": updated_project.teck_stack,
            "github_repo": updated_project.github_repo,
        },
    }


@app.delete("/portfolio/{project_id}")
def remove_portfolio(
    project_id: int, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user) # Security lock
):
    deleted_project = delete_portfolio(db=db, project_id=project_id)

    if deleted_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found",
        )

    return {
        "message": f"Project with ID {project_id} deleted successfully",
        "deleted_id": project_id,
    }


# =========================================
# AI EMAIL AGENT (SECURED)
# =========================================
@app.post("/email")
def generate_email(
    request: EmailRequest,
    current_user: str = Depends(get_current_user) # Security lock
):
    try:
        email_data = get_cold_email(url=request.url, name=request.name)
        return {"email": email_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))