from sqlalchemy.orm import Session

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


# =========================================
# ADD PORTFOLIO
# =========================================

def add_portfolio(
    db: Session,
    project_id: int,
    project_name: str,
    teck_stack: str,
    github_repo: str
):

    new_portfolio = Portfolio(

        Project_id=project_id,

        Project_name=project_name,

        teck_stack=teck_stack,

        github_repo=github_repo
    )

    db.add(new_portfolio)

    db.commit()

    db.refresh(new_portfolio)

    return new_portfolio