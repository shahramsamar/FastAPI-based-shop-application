# Import necessary modules from SQLAlchemy to manage database connection and session handling.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database.config import settings  # Import settings from the configuration file to get DATABASE_URL

# Set up the SQLAlchemy database URL from the settings.
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create the database engine using the database URL.
# The 'connect_args' parameter is needed for SQLite, specifically to allow multi-threaded access.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Disable the check for the same thread (SQLite specific)
)

# SessionLocal is a session factory that is configured to create sessions bound to the engine.
# Sessions allow interaction with the database and are not committed or flushed automatically.
SessionLocal = sessionmaker(autocommit=False,  # Disable autocommit to handle transactions manually.
                            autoflush=False,   # Disable autoflush so data is not sent to the DB until explicitly committed.
                            bind=engine)      # Bind the session to the engine for database interaction.

# Base class to define models that will be mapped to tables in the database.
# All models should inherit from this base class.
Base = declarative_base()

# Dependency function to provide database sessions to route handlers or functions.
# It uses a context manager to ensure the session is properly closed after use.
def get_db():
    db = SessionLocal()  # Create a new session.
    try:
        yield db  # Yield the session to the caller.
    finally:
        db.close()  # Ensure the session is closed after use, even if an error occurs.

# Function to initiate the database by creating all the tables defined in the models.
# It uses the metadata of the Base class to generate the tables in the database.
def initiate_database():
    Base.metadata.create_all(bind=engine)  # Create all tables in the database according to the models.
