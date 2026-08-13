from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from Backend.Databases.database import Base, engine, get_db
from Backend.auth import register_user, login_user
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
# from Backend.agents.cold_mail_agent import get_cold_email


app = FastAPI(title="PitStop AI")


Base.metadata.create_all(bind=engine)
# Serve FRONTEND folder
app.mount(
    "/static",
    StaticFiles(directory="FRONTEND"),
    name="static"
)


# Serve index.html
@app.get("/")
def home():

    return FileResponse(
        "FRONTEND/index.html"
    )


class RegisterRequest(BaseModel):

    name: str
    email: str
    password: str


class LoginRequest(BaseModel):

    email: str
    password: str



@app.get("/")
def home():

    return {"message": "PitStop AI Backend is running"}

@app.post("/register")
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):

    user = register_user(
        db=db, name=user_data.name, email=user_data.email, password=user_data.password
    )

    if user is None:

        raise HTTPException(status_code=400, detail="Email already registered")

    return {
        "message": "Registration successful",
        "user": {"id": user.id, "name": user.name, "email": user.email},
    }


@app.post("/login")
def login(user_data: LoginRequest, db: Session = Depends(get_db)):

    user = login_user(db=db, email=user_data.email, password=user_data.password)

    if user is None:

        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "user": {"id": user.id, "name": user.name, "email": user.email},
    }


# @app.get("/mail")
# def get_data():
#     return get_cold_email()
