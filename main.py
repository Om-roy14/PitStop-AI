from typing import List, Optional
from Backend.functions.portfolio_acccess import (
    add_portfolio,
    delete_portfolio,
    get_all_portfolios,
    get_portfolio_by_id,
    update_portfolio,

)
from Backend.auth import (

    login_user,
    register_user,
)
from Backend.Databases.database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

# =========================================
# APP & DATABASE
# =========================================

app = FastAPI(title="PitStop AI")

Base.metadata.create_all(bind=engine)

# =========================================
# FRONTEND
# =========================================

app.mount("/static", StaticFiles(directory="FRONTEND"), name="static")


@app.get("/")
def home():
  return FileResponse("FRONTEND/index.html")


@app.get("/dashboard")
def portfolio_ui():
  return FileResponse("FRONTEND/index1.html")


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

  # FIX: Required for reading SQLAlchemy ORM objects
  model_config = ConfigDict(from_attributes=True)


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
      "user": {
          "id": user.id,
          "name": user.name,
          "email": user.email,
          "linkedin_id": user.linkedin_id,
          "github_id": user.github_id,
      },
  }


# =========================================
# PORTFOLIO CRUD
# =========================================


# FIX: Changed path from "/portfolios" to "/portfolio"
@app.post("/portfolio", status_code=status.HTTP_201_CREATED)
def add_project(
    portfolio_data: PortfolioRequest, db: Session = Depends(get_db)
):
  # Check if project ID already exists
  existing = get_portfolio_by_id(
      db=db, project_id=portfolio_data.Project_id
  )
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
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
  return get_all_portfolios(db=db, skip=skip, limit=limit)


@app.get("/portfolio/{project_id}", response_model=PortfolioResponse)
def read_single_portfolio(project_id: int, db: Session = Depends(get_db)):
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
def remove_portfolio(project_id: int, db: Session = Depends(get_db)):
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