# ------------------------------------------------------------
# Backend Developer (Intern) Assignment
# Author: Vaibhav Singh
# Date: 30 October 2024
#
# This is the main entry point of the FastAPI backend.
# It connects the database, sets up routes, and serves the frontend.
# ------------------------------------------------------------

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from app.database import Base, engine
import app.models as models

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Task Management API (FastAPI)")

# Create all database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Mount static frontend directory
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# Import and register routers for authentication and task CRUD
from app import auth, crud

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(crud.router, prefix="/api/v1/tasks", tags=["Tasks"])

# Simple startup log
print("🚀 FastAPI app by Vaibhav Singh is running successfully!")
