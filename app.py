
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager
from dotenv import load_dotenv

from datetime import datetime
import os

# ==========================================
# LOAD ENV
# ==========================================

load_dotenv()

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

# ==========================================
# IMPORTS
# ==========================================

from src.website_analyzer import (
    analyze_website
)

# ==========================================
# LIFESPAN
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("=" * 50)
    print("Omminsentiry AI Started")
    print("=" * 50)

    yield

    print("=" * 50)
    print("Omminsentiry AI Stopped")
    print("=" * 50)


# ==========================================
# APP
# ==========================================

app = FastAPI(
    title="Omminsentiry AI",
    description="AI Website Trust Verification",
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
# STATIC
# ==========================================

app.mount(
    "/static",
    StaticFiles(
        directory="static"
    ),
    name="static"
)

# ==========================================
# TEMPLATES
# ==========================================

templates = Jinja2Templates(
    directory="templates"
)

# ==========================================
# HOME
# ==========================================

@app.get("/")
async def home(
    request: Request
    ):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )

# ==========================================
# MAP PAGE
# ==========================================

@app.get("/map")
async def map_page(
    request: Request
):

    return templates.TemplateResponse(
        "map.html",
        {
            "request": request
        }
    )

# ==========================================
# HEALTH
# ==========================================

@app.get("/health")
async def health():

    return {

        "status":
            "online",

        "service":
            "Omminsentiry AI",

        "timestamp":
            datetime.utcnow().isoformat()
    }

# ==========================================
# CHECK DOMAIN
# ==========================================

@app.get("/check/{domain}")
async def check_domain(
    domain: str
):

    try:

        report = analyze_website(
            domain
        )

        return {

            "success":
                True,

            "timestamp":
                datetime.utcnow().isoformat(),

            "data":
                report
        }

    except Exception as e:

        return {

            "success":
                False,

            "error":
                str(e)
        }

# ==========================================
# SCORE ONLY
# ==========================================

@app.get("/score/{domain}")
async def score(
    domain: str
):

    try:

        report = analyze_website(
            domain
        )

        return {

            "success":
                True,

            "domain":
                domain,

            "trust_score":
                report.get(
                    "trust_score",
                    0
                )
        }

    except Exception as e:

        return {

            "success":
                False,

            "error":
                str(e)
        }

# ==========================================
# FULL REPORT (JSON)
# ==========================================

@app.get("/report/{domain}")
async def report(
    domain: str
):

    try:

        data = analyze_website(
            domain
        )

        return {

            "success":
                True,

            "report":
                data
        }

    except Exception as e:

        return {

            "success":
                False,

            "error":
                str(e)
        }


# ==========================================
# VIEW HTML REPORT
# ==========================================

@app.get("/report/view/{domain}")
async def view_report(
    request: Request,
    domain: str
):

    try:

        data = analyze_website(
            domain
        )

        return templates.TemplateResponse(
            request=request,
            name="report.html",
            context={
                "request": request,
                "report": data
            }
        )

    except Exception as e:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "error": str(e)
            }
        )


# ==========================================
# RAW DATA COLLECTION
# ==========================================

from src.data_collected import collect_data

@app.get("/data/{domain}")
async def data_route(
        domain: str
    ):

    try:

        data = collect_data(
            domain
        )

        return {
            "success": True,
            "data": data
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }




# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

