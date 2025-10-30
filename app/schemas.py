# ------------------------------------------------------------
# Pydantic Schemas
# Author: Vaibhav Singh
# Date: 30 October 2024
#
# This file defines the data validation and response models
# using Pydantic for the FastAPI application.
# These models ensure clean input/output data handling.
# ------------------------------------------------------------

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ------------------------------
# User Schemas
# ------------------------------
class UserCreate(BaseModel):
    """Schema for creating a new user"""
    email: EmailStr
    password: str
    role: Optional[str] = "user"


class UserOut(BaseModel):
    """Schema for returning user info"""
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True  # updated name from orm_mode in Pydantic v2


# ------------------------------
# Authentication Schema
# ------------------------------
class Token(BaseModel):
    """Schema for returning JWT access token"""
    access_token: str


# ------------------------------
# Task Schemas
# ------------------------------
class TaskCreate(BaseModel):
    """Schema for creating or updating a task"""
    title: str
    description: Optional[str] = ""


class TaskOut(BaseModel):
    """Schema for showing task details"""
    id: int
    title: str
    description: Optional[str]
    owner_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True  # replaces orm_mode
