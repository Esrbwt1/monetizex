# main.py
from fastapi import FastAPI
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, init_db, EmailSignup
from fastapi.middleware.cors import CORSMiddleware


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
    
# Define a model for content input
class ContentData(BaseModel):
    content: str


# Create an instance of the FastAPI class
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with the specific origin of your GitHub Pages if you want to restrict access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/signups")
def read_signups(db: Session = Depends(get_db)):
    # Query all email sign-ups from the database.
    signups = db.query(EmailSignup).all()
    # Create a list of email addresses to return.
    emails = [signup.email for signup in signups]
    return {"signups": emails}

@app.post("/monetize")
def monetize_content(data: ContentData):
    # Extract the content from the request
    content = data.content
    
    # Dummy analysis: simulate AI by checking for keywords.
    # (In the future, this is where you could integrate a call to an AI service like OpenAI's API.)
    if "video" in content.lower():
        strategy = "Integrate video ads and seek sponsorship opportunities."
    elif "blog" in content.lower():
        strategy = "Consider affiliate marketing and sponsored posts."
    elif "podcast" in content.lower():
        strategy = "Explore podcast sponsorships and premium content subscriptions."
    else:
        strategy = "Consider a mix of affiliate marketing, digital products, and display ads."
    
    # Return the simulated monetization strategy as JSON.
    return {"strategy": strategy}
