import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI, Request

from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager
from dotenv import load_dotenv

from datetime import datetime
import os

from src.omnipop.phishing_detector import detect_phishing
from src.omnipop.threat_detector import detect_threat
from src.omnipop.page_analyzer import analyze_page
from src.omnipop.behavior_analyzer import analyze_behavior
from src.omnipop.fraud_detector import detect_fraud
from src.omnipop.payment_detector import detect_payment_request
from src.omnipop.popup_generator import generate_popup
from src.omnipop.report_sender import create_report
from src.omnipop.training_data import build_training_data

from src.scam_feed_collector import (
    collect_scam_feeds
)

from src.phishing_feed import (
    get_phishing_feed
)

from src.reputation_cache import (
    cache_size,
    clear_cache
)


from backend.api_routes import router as backend_router
import pickle

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "trust_model.pkl"), "rb") as f:
    trust_model = pickle.load(f)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "omnipop_model.pkl"), "rb") as f:
    omnipop_model = pickle.load(f)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "phishing_model.pkl"), "rb") as f:
    phishing_model = pickle.load(f)
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

app.include_router(backend_router)

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
# STATIC & TEMPLATES
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount(
    "/static",
    StaticFiles(
        directory=os.path.join(BASE_DIR, "static")
    ),
    name="static"
)

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
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
        request=request,
        name="map.html",
        context={
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
# INFO
# ==========================================

@app.get("/info")
async def info():
    return {
        "name": "Omminsentiry AI",
        "description": "AI Website Trust Verification System",
        "version": "0.1.0"
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
@app.get("/omnipop")
async def omnipop_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="omnipop.html",
        context={
            "request": request
        }
    )
@app.get("/dashboard")
async def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request
        }
    )


@app.get("/admin/login")
async def admin_login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin_login.html",
        context={
            "request": request
        }
    )


@app.get("/about")
async def about_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={
            "request": request
        }
    )


@app.get("/contact")
async def contact_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="contact.html",
        context={
            "request": request
        }
    )


@app.get("/services")
async def services_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="services.html",
        context={
            "request": request
        }
    )



#Trust Prediction Route

@app.get("/ai/trust/{domain}")
async def ai_trust(domain: str):

    report = analyze_website(domain)

    prediction = trust_model.predict([
        [
            int(report["registered"]),
            report["age_days"],
            int(report["ssl"]),
            report["reputation"]["score"],
            report["trust_score"]
        ]
    ])

    return {

        "success": True,

        "domain": domain,

        "trust_score":
            report["trust_score"],

        "prediction":
            int(prediction[0])
    }

#Phishing Detection
@app.get("/ai/phishing")
async def phishing_test():

    prediction = phishing_model.predict([
        [
            1,  # fake_login
            1,  # password_collection
            1   # brand_impersonation
        ]
    ])

    return {

        "success": True,

        "phishing_detected":
            bool(prediction[0])
    }


# Threat detect
@app.post("/omnipop/threat-detect")
async def threat_detect(payload: dict):

    result = detect_threat(
        payload.get("content", "")
    )

    return result


@app.post("/omnipop/page-analyze")
async def page_analyze(payload: dict):

    return analyze_page(
        payload.get("html", "")
    )

@app.post("/omnipop/behavior")
async def behavior(payload: dict):

    return analyze_behavior(
        payload.get("content", "")
    )


@app.post("/omnipop/fraud")
async def fraud(payload: dict):
    return detect_fraud(
        payload.get("content", "")
    )

@app.post("/omnipop/phishing")
async def phishing(payload: dict):
    return {

        "phishing":
            detect_phishing(
                payload.get(
                    "content",
                    ""
                )
            )["is_phishing"]
    }

@app.post("/omnipop/payment")
async def payment(payload: dict):

    return {

        "payment_detected":
            detect_payment_request(
                payload.get(
                    "content",
                    ""
                )
            )
    }

@app.get("/omnipop/popup/{risk_score}")
async def popup(risk_score: int):

    return generate_popup(
        risk_score
    )

@app.post("/omnipop/report")
async def report(payload: dict):

    return create_report(

        payload.get(
            "domain"
        ),

        payload.get(
            "threats",
            []
        ),

        payload.get(
            "risk_score",
            0
        )
    )


@app.get("/omnipop/training-data")
async def training_data_route():

    df = build_training_data()

    return df.to_dict(
        orient="records"
    )


@app.post("/omnipop/train")
async def train_omnipop_models():
    try:
        from sklearn.ensemble import RandomForestClassifier
        import pandas as pd
        import pickle

        # 1. Train OmniPop Model
        df_op = build_training_data()
        X_op = df_op[["credit_card_request", "urgency_language", "phishing"]]
        y_op = df_op["label"]
        model_op = RandomForestClassifier(n_estimators=100, random_state=42)
        model_op.fit(X_op, y_op)
        with open("models/omnipop_model.pkl", "wb") as f:
            pickle.dump(model_op, f)

        # 2. Train Phishing Model
        data_phish = pd.DataFrame({
            "fake_login": [0,0,1,1,1,1],
            "password_collection": [0,1,1,1,1,1],
            "brand_impersonation": [0,0,0,1,1,1],
            "label": [0,0,1,1,1,1]
        })
        X_p = data_phish[["fake_login", "password_collection", "brand_impersonation"]]
        y_p = data_phish["label"]
        model_p = RandomForestClassifier(n_estimators=100, random_state=42)
        model_p.fit(X_p, y_p)
        with open("models/phishing_model.pkl", "wb") as f:
            pickle.dump(model_p, f)

        # Reload models globally in app.py
        global omnipop_model, phishing_model
        omnipop_model = model_op
        phishing_model = model_p

        return {
            "success": True,
            "message": "OmniPop & Phishing models retrained successfully."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }




#Threat Detector Route
@app.get("/test/threat")
async def test_threat():

    content = """
    Act now.

    Verify account immediately.

    Enter password.

    Submit your credit card.
    """

    result = detect_threat(
        content
    )

    return result

# Payment Request Test
@app.get("/test/payment-threat")
async def test_payment_threat():

    content = """
    Please enter your credit card
    information to continue.
    """

    result = detect_threat(
        content
    )

    return result

# Safe Website Test Route
@app.get("/test/phishing-safe")
async def test_phishing_safe():

    content = """
    Welcome to our company website.
    Browse products and services.
    """

    result = detect_phishing(
        content
    )

    return {

        "test":
            "phishing_detector_safe",

        "phishing_detected":
            result["is_phishing"]
    }

#Urgency Language Test
@app.get("/test/urgency-threat")
async def test_urgency_threat():

    content = """
    Act now.
    Verify immediately.
    Limited time offer.
    """

    result = detect_threat(
        content
    )

    return result




#  OmniPop Diagnostics Route
@app.get("/omnipop/diagnostics")
async def omnipop_diagnostics():

    phishing_content = """
    Login now.
    Verify account.
    Enter password.
    """

    threat_content = """
    Act now.
    Verify immediately.
    Submit credit card.
    """

    phishing_result = detect_phishing(
        phishing_content
    )

    threat_result = detect_threat(
        threat_content
    )

    return {

        "status":
            "online",

        "phishing_detector":
            phishing_result,

        "threat_detector":
            threat_result
    }


# Scam Feed Route
@app.get("/threat/scams")
async def scam_feed():

    return collect_scam_feeds()

# Phishing Feed Route
@app.get("/threat/phishing")
async def phishing_feed_route():

    return get_phishing_feed()


# Reputation Cache Status
@app.get("/cache/status")
async def cache_status():

    return cache_size()

# Clear Reputation Cache
@app.get("/cache/clear")
async def cache_clear():

    return clear_cache()
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

