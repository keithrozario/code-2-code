from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.moneynote.models.base import Base

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/db/moneynote.db"

# Create the SQLAlchemy engine
# connect_args is needed for SQLite to allow multiple threads to access the database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create database tables (if they don't exist)
# This is for initial setup; in production, you'd use Alembic migrations
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
