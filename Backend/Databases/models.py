from sqlalchemy import Column, Integer, String

from Backend.Databases.database import Base


# =========================================
# USER
# =========================================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String(255),
        nullable=False
    )

    linkedin_id = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    github_id = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )


# =========================================
# PORTFOLIO
# =========================================

class Portfolio(Base):

    __tablename__ = "portfolio"

    Project_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    Project_name = Column(
        String(100),
        nullable=False
    )

    teck_stack = Column(
        String(150),
        nullable=False
    )

    github_repo = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )