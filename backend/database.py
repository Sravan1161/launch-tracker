from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite for simplicity during development.
# For production, swap this connection string for a Postgres URL —
# SQLAlchemy makes that a one-line change since we're not writing raw SQL.
SQLALCHEMY_DATABASE_URL = "sqlite:///./launch_tracker.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency for FastAPI routes — yields a session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
