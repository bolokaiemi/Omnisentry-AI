
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager
from dotenv import load_dotenv

import os
from datetime import datetime

# ==========================================
# LOAD ENV
# ==========================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ==========================================
# IMPORT ANALYZER
# ==========================================

from src.website_analyzer import analyze_website

# ==========================================
# LIFESPAN
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("=" * 50)
    print("Omminsentiry AI Started")
    print("Loading Security Modules...")
    print("=" * 50)

    yield

    print("=" * 50)
    print("Omminsentiry AI Stopped")
    print("=" * 50)

# ==========================================
# APP
# ==========================================

app = FastAPI(
    title="Omminsentiry AI Security Check",
    description="AI-Powered Website Trust Verification Platform",
    version="0.1.0",
    lifespan=lifespan
)

# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ==========================================
# STATIC FILES
# ==========================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# ==========================================
# TEMPLATES
# ==========================================

templates = Jinja2Templates(directory="templates")

# ==========================================
# HOME PAGE (ONLY ONCE)
# ==========================================

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

# ==========================================
# HEALTH
# ==========================================

@app.get("/health")
async def health():

    return {
        "status": "online",
        "service": "Omminsentiry AI",
        "timestamp": datetime.utcnow().isoformat()
    }

# ==========================================
# INFO
# ==========================================

@app.get("/info")
async def info():

    return {
        "name": "Omminsentiry AI",
        "version": "0.1.0",
        "features": [
            "SSL Check",
            "Domain Analysis",
            "Reputation Check",
            "Trust Scoring"
        ]
    }

# ==========================================
# CHECK WEBSITE
# ==========================================

@app.get("/check/{domain}")
async def check_domain(domain: str):

    try:

        report = analyze_website(domain)

        return {
            "success": True,
            "timestamp": datetime.utcnow().isoformat(),
            "data": report
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

# ==========================================
# SCORE
# ==========================================

@app.get("/score/{domain}")
async def trust_score(domain: str):

    try:

        report = analyze_website(domain)

        return {
            "success": True,
            "domain": domain,
            "trust_score": report.get("trust_score", 0)
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

# ==========================================
# HTTPS
# ==========================================

@app.get("/https/{domain}")
async def https_status(domain: str):

    try:

        report = analyze_website(domain)

        return {
            "success": True,
            "https": report.get("ssl", False)
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

# ==========================================
# REPUTATION
# ==========================================

@app.get("/reputation/{domain}")
async def reputation(domain: str):

    try:

        report = analyze_website(domain)

        return {
            "success": True,
            "reputation": report.get("reputation", "UNKNOWN")
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

# ==========================================
# FULL REPORT
# ==========================================

@app.get("/report/{domain}")
async def full_report(domain: str):

    try:

        report = analyze_website(domain)

        return {
            "success": True,
            "generated": datetime.utcnow().isoformat(),
            "report": report
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

