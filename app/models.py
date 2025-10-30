# ------------------------------------------------------------
# Database Models
# Author: Vaibhav Singh
# Date: 30 October 2024
#
# This file defines all ORM models using SQLAlchemy.
# It includes two main entities:
#   1. User  → Stores registered users and their roles
#   2. Task  → Stores user-created tasks (linked to User)
# ------------------------------------------------------------

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


# ------------------------------
# User Model
# ------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(20), default="user")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship → one user can have multiple tasks
    tasks = relationship("Task", back_populates="owner")

    def __repr__(self):
        return f"<User(email={self.email}, role={self.role})>"


# ------------------------------
# Task Model
# ------------------------------
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

