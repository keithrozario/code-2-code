import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

from database import Base, get_db
import models

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the test database
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for a test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


def test_database_connection(db_session):
    """Test that a connection can be made to the database."""
    try:
        result = db_session.execute(text("SELECT 1"))
        assert result.scalar() == 1
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")


def test_get_db_dependency():
    """Test the get_db dependency generator."""
    try:
        db_gen = get_db()
        db = next(db_gen)
        assert db is not None
        # Check if it's a session
        assert hasattr(db, "query")
    finally:
        # Simulate closing the session
        with pytest.raises(StopIteration):
            next(db_gen)


def test_model_creation():
    """Test that the tables were created correctly."""
    inspector = text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    with engine.connect() as connection:
        result = connection.execute(inspector)
        tables = [row[0] for row in result]
        assert "users" in tables
        assert "groups" in tables


# Cleanup the test database file after tests are done
@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Cleanup a testing database."""

    def remove_test_db():
        if os.path.exists("./test.db"):
            os.remove("./test.db")

    request.addfinalizer(remove_test_db)
