from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import uuid
from datetime import datetime


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class PortfolioSection(BaseModel):
    id: str
    title: str
    subtitle: str = ""
    description: str
    image_url: str = ""
    features: List[str] = []
    
class ContactSubmission(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ContactCreate(BaseModel):
    name: str
    email: str
    message: str

# Portfolio data
PORTFOLIO_DATA = {
    "hero": {
        "id": "hero",
        "title": "Emergent Labs",
        "subtitle": "AI-Powered Application Development Platform",
        "description": "The world's first truly agentic coding platform that helps developers build complete applications through conversational AI. From setup to deployment, we handle it all.",
        "image_url": "https://images.unsplash.com/photo-1724190168156-e93ba2bfd041?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwyfHxBSSUyMGRldmVsb3BtZW50fGVufDB8fHx8MTc1NTA2MzA5MXww&ixlib=rb-4.1.0&q=85",
        "features": ["Conversational Interface", "Full-Stack Development", "Built-in Deployment", "AI-Powered Coding"]
    },
    "services": {
        "id": "services",
        "title": "Core Services",
        "subtitle": "What We Offer",
        "description": "Comprehensive AI-powered development solutions for all your application needs.",
        "image_url": "https://images.unsplash.com/photo-1738003946582-aabeabf5e009?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwzfHxBSSUyMGRldmVsb3BtZW50fGVufDB8fHx8MTc1NTA2MzA5MXww&ixlib=rb-4.1.0&q=85",
        "features": [
            "AI-powered full-stack application development",
            "Conversational interface for building apps (not form-based builders)",
            "Complete project lifecycle management from setup to deployment",
            "Built-in deployment, authentication, and infrastructure handling"
        ]
    },
    "users": {
        "id": "users",
        "title": "Target Users",
        "subtitle": "Who We Serve",
        "description": "Designed for developers, founders, and teams who want to build faster and more efficiently.",
        "image_url": "https://images.unsplash.com/photo-1688733720228-4f7a18681c4f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwxfHxjb2RpbmclMjBwbGF0Zm9ybXxlbnwwfHx8fDE3NTUwNjMxMDJ8MA&ixlib=rb-4.1.0&q=85",
        "features": [
            "Developers who want to build faster",
            "PMs and operators building internal tools",
            "Solo founders and tech teams shipping MVPs and beyond",
            "Individuals with zero coding experience looking to build their first product"
        ]
    },
    "differentiators": {
        "id": "differentiators",
        "title": "Key Differentiators",
        "subtitle": "What Makes Us Unique",
        "description": "Revolutionary approach to application development with AI at the core.",
        "image_url": "https://images.pexels.com/photos/8438944/pexels-photo-8438944.jpeg",
        "features": [
            "World's first truly agentic vibe coding platform",
            "Conversational interface rather than traditional form-based builders",
            "Handles deployment, auth, and infrastructure from day one",
            "Focuses on both first mile (setup) and last mile (deploy & monitor)"
        ]
    },
    "capabilities": {
        "id": "capabilities",
        "title": "Technical Capabilities",
        "subtitle": "Powerful Technology Stack",
        "description": "Comprehensive development capabilities across web and mobile platforms.",
        "image_url": "https://images.unsplash.com/photo-1607743386830-f198fbd7f9c4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwzfHxjb2RpbmclMjBwbGF0Zm9ybXxlbnwwfHx8fDE3NTUwNjMxMDJ8MA&ixlib=rb-4.1.0&q=85",
        "features": [
            "Web application development (React + FastAPI + MongoDB, Next.js)",
            "Mobile application development (Expo framework) - available for subscribed users",
            "Built-in GitHub integration for version control",
            "Live preview and testing capabilities",
            "Custom domain support for deployments",
            "AI integrations through Emergent LLM Key"
        ]
    },
    "features": {
        "id": "features",
        "title": "Platform Features",
        "subtitle": "Complete Development Environment",
        "description": "Everything you need to build, test, and deploy applications in one platform.",
        "image_url": "https://images.unsplash.com/photo-1724190168156-e93ba2bfd041?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwyfHxBSSUyMGRldmVsb3BtZW50fGVufDB8fHx8MTc1NTA2MzA5MXww&ixlib=rb-4.1.0&q=85",
        "features": [
            "Multiple AI agents (E1 stable, E1.1 experimental, Mobile Agent)",
            "Pro Mode for creating custom agents",
            "Credit-based pricing system",
            "Built-in testing and deployment tools",
            "Chat forking for managing complex projects"
        ]
    }
}

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Emergent Labs API"}

@api_router.get("/portfolio", response_model=Dict[str, PortfolioSection])
async def get_portfolio_data():
    return PORTFOLIO_DATA

@api_router.get("/portfolio/{section_id}")
async def get_portfolio_section(section_id: str):
    if section_id in PORTFOLIO_DATA:
        return PORTFOLIO_DATA[section_id]
    return {"error": "Section not found"}

@api_router.post("/contact", response_model=ContactSubmission)
async def submit_contact(contact: ContactCreate):
    contact_dict = contact.dict()
    contact_obj = ContactSubmission(**contact_dict)
    await db.contact_submissions.insert_one(contact_obj.dict())
    return contact_obj

@api_router.get("/contact", response_model=List[ContactSubmission])
async def get_contact_submissions():
    submissions = await db.contact_submissions.find().to_list(1000)
    return [ContactSubmission(**submission) for submission in submissions]

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()