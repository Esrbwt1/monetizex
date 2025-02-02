# main.py
from fastapi import FastAPI
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, init_db, EmailSignup

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define a Pydantic model for the email signup data
class EmailSignupCreate(BaseModel):
    email: str

# Create an instance of the FastAPI class
app = FastAPI()
init_db()

# Define a route (endpoint) that returns a simple message
@app.get("/")
def read_root():
    return {"message": "Hello, MonetizeX! Your API is up and running."}

@app.post("/signup")
def create_email_signup(signup: EmailSignupCreate, db: Session = Depends(get_db)):
    # Check if the email already exists in the database.
    existing_signup = db.query(EmailSignup).filter(EmailSignup.email == signup.email).first()
    if existing_signup:
        raise HTTPException(status_code=400, detail="Email already signed up")
    
    # Create a new email signup record.
    new_signup = EmailSignup(email=signup.email)
    db.add(new_signup)
    db.commit()
    db.refresh(new_signup)
    
    return {"message": "Thank you for signing up!", "email": new_signup.email}
