from sqlalchemy.orm import Session
from typing import Optional

from Backend.Databases.models import User, Portfolio


# =========================================
# REGISTER
# =========================================

def register_user(
    db: Session,
    name: str,
    email: str,
    password: str,
    linkedin_id: str,
    github_id: str
):

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        return None

    new_user = User(
        name=name,
        email=email,
        password=password,
        linkedin_id=linkedin_id,
        github_id=github_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =========================================
# LOGIN
# =========================================

def login_user(
    db: Session,
    email: str,
    password: str
):

    user = (
        db.query(User)
        .filter(
            User.email == email,
            User.password == password
        )
        .first()
    )

    return user
