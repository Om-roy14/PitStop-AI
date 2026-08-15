from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from Backend.Databases.database import (
    Base,
    engine,
    get_db
)

from Backend.auth import (
    register_user,
    login_user
)

# from Backend.agents.cold_mail_agent import get_cold_email


# =========================================
# APP
# =========================================

app = FastAPI(
    title="PitStop AI"
)


# =========================================
# DATABASE
# =========================================

Base.metadata.create_all(
    bind=engine
)


# =========================================
# FRONTEND
# =========================================

app.mount(
    "/static",
    StaticFiles(directory="FRONTEND"),
    name="static"
)


@app.get("/")
def home():

    return FileResponse(
        "FRONTEND/index.html"
    )


# =========================================
# REQUEST MODELS
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


# =========================================
# REGISTER
# =========================================

@app.post("/register")
def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):

    user = register_user(

        db=db,

        name=user_data.name,

        email=user_data.email,

        password=user_data.password,

        linkedin_id=user_data.linkedin_id,

        github_id=user_data.github_id
    )


    if user is None:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )


    return {

        "message": "Registration successful",

        "user": {

            "id": user.id,

            "name": user.name,

            "email": user.email,

            "linkedin_id": user.linkedin_id,

            "github_id": user.github_id
        }
    }


# =========================================
# LOGIN
# =========================================

@app.post("/login")
def login(
    user_data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = login_user(

        db=db,

        email=user_data.email,

        password=user_data.password
    )


    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    return {

        "message": "Login successful",

        "user": {

            "id": user.id,

            "name": user.name,

            "email": user.email,

            "linkedin_id": user.linkedin_id,

            "github_id": user.github_id
        }
    }


# =========================================
# COLD EMAIL
# =========================================

# @app.get("/mail")
# def get_data():
#
#     return get_cold_email()