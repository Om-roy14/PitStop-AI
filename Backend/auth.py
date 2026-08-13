from sqlalchemy.orm import Session

from Backend.Databases.models import User


# =========================================
# REGISTER
# =========================================

def register_user(
    db: Session,
    name: str,
    email: str,
    password: str
):

    # Check whether email already exists

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:

        return None


    # Create user

    new_user = User(
        name=name,
        email=email,
        password=password
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
