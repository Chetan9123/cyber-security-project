from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import scam_detection, complaint
from database import Base, engine


# Create DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Powered Crime Complaint Management Backend",
    description="Backend for complaint management and scam detection",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(scam_detection.router)
app.include_router(complaint.router)

@app.get("/")
def home():
    return {"message": "🚀 Crime Complaint Management System API is running!"}



app = FastAPI()

# Include router
app.include_router(scam_detection.router)