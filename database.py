# database.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a SQLite database called 'monetizex.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///./monetizex.db"

# Create an engine to connect to the SQLite database.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a session local class for database operations.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our models.
Base = declarative_base()

# Define a simple model to store email sign-ups.
class EmailSignup(Base):
    __tablename__ = "email_signups"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)

# Create the tables in the database.
def init_db():
    Base.metadata.create_all(bind=engine)