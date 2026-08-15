from sqlalchemy import Column, Integer, String

from Backend.Databases.database import Base


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
