# ------------------------------------------------------------
# Database Configuration File
# Author: Vaibhav Singh
# Date: 30 October 2024
#
# This file handles the database connection setup for the app
# using SQLAlchemy ORM with environment variable support.
# ------------------------------------------------------------

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetch the database URL (default to SQLite for local development)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Create SQLAlchemy engine
# The 'check_same_thread' argument is required only for SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()

# Optional confirmation message
print(" Database connection initialized successfully by Vaibhav Singh.")
