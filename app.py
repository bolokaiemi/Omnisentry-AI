import sys

import os



sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI, Request, Form

from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from datetime import datetime, timezone, timedelta
import random
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

try:
    from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
except ImportError:  # pragma: no cover
    FastMail = None
    MessageSchema = None
    ConnectionConfig = None
from pydantic import EmailStr
from dotenv import load_dotenv

load_dotenv()




# ============================================================
# FASTAPI-MAIL CONFIGURATION
# ============================================================

if ConnectionConfig and FastMail:
    mail_config = ConnectionConfig(
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_FROM=os.getenv("MAIL_FROM"),
        MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
        MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )
    fastmail = FastMail(mail_config)
else:
    mail_config = None



# ============================================================
# CONFIRMATION EMAIL
# ============================================================

async def send_confirmation_email(
    email: EmailStr,
    username: str,
    confirmation_token: str
):
    confirmation_link = (
        f"http://localhost:8000/confirm-email/"
        f"{confirmation_token}"
    )

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Confirm Your Email</title>
    </head>

    <body style="
        margin: 0;
        padding: 0;
        background-color: #f4f7fb;
        font-family: Arial, sans-serif;
    ">

        <div style="
            max-width: 600px;
            margin: 40px auto;
            background: #ffffff;
            padding: 35px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        ">

            <h1 style="
                color: #2563eb;
                text-align: center;
            ">
                Welcome!
            </h1>

            <h2>
                Hello {username},
            </h2>

            <p style="
                font-size: 16px;
                line-height: 1.6;
                color: #444;
            ">
                Thank you for registering with our platform.
                Please confirm your email address to activate
                your account.
            </p>

            <div style="text-align: center; margin: 30px 0;">

                <a href="{confirmation_link}"
                   style="
                       display: inline-block;
                       padding: 14px 28px;
                       background-color: #2563eb;
                       color: #ffffff;
                       text-decoration: none;
                       border-radius: 8px;
                       font-weight: bold;
                   ">
                    Confirm My Email
                </a>

            </div>

            <p style="
                font-size: 14px;
                color: #777;
                line-height: 1.5;
            ">
                If you did not create an account, you can safely
                ignore this email.
            </p>

            <hr style="
                border: 0;
                border-top: 1px solid #eeeeee;
                margin: 30px 0;
            ">

            <p style="
                text-align: center;
                font-size: 12px;
                color: #999;
            ">
                © 2026 Your Platform. All rights reserved.
            </p>

        </div>

    </body>
    </html>
    """

    message = MessageSchema(
        subject="Confirm Your Email Address",
        recipients=[email],
        body=html_content,
        subtype="html",
    )

    if mail_config and FastMail:
        fast_mail = FastMail(mail_config)
        await fast_mail.send_message(message)

from contextlib import asynccontextmanager




import os
import uuid

from datetime import datetime, timedelta
from fastapi import Form, Request
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

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

# Load ML models with safe error handling
def _load_model(path):
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print(f"[WARN] Failed to load model {os.path.basename(path)}: {e}")
        return None

trust_model = _load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "trust_model.pkl"))
omnipop_model = _load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "omnipop_model.pkl"))
phishing_model = _load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "phishing_model.pkl"))
# ==========================================
# LOAD ENV
# ==========================================

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

# ==========================================
# IMPORTS
# ==========================================

from src.website_analyzer import (
    analyze_website
)
# Removed duplicate FastAPI app initialization and static mount; using the later defined app with lifespan and proper middleware.



# ==========================================
# LIFESPAN
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("=" * 50)
    print("Omnisentry AI Started")
    print("=" * 50)

    yield

    print("=" * 50)
    print("Omnisentry AI Stopped")
    print("=" * 50)


# ==========================================
# APP
# ==========================================

# Removed earlier FastAPI initialization (duplicate app instance).
app = FastAPI(
    title="Omnisentry AI",
    description="AI Website Trust Verification",
    version="0.1.0",
    lifespan=lifespan
)


# ==============================
# SESSION MIDDLEWARE
# ==============================
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "change-this-secret-key")
)
app.include_router(backend_router)


# ==============================
# AUTH DEPENDENCY
# ==============================
from fastapi import Depends, HTTPException
from fastapi.responses import RedirectResponse

def require_auth(request: Request):
    """
    Protect a route with the current login session.

    FastAPI dependencies cannot stop route execution merely by returning
    a RedirectResponse, so raise an HTTP 303 with a Location header.
    """
    if not request.session.get("username"):
        raise HTTPException(
            status_code=303,
            headers={"Location": "/login"}
        )
    return True


from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Hide unhashable dict errors from client
    if isinstance(exc, TypeError) and "unhashable type" in str(exc):
        return JSONResponse(status_code=400, content={"detail": "Invalid request payload"})
    print(f"[ERROR] Unhandled exception: {exc}")
    return JSONResponse(status_code=500, content={"detail": str(exc)})

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

@app.get("/", dependencies=[Depends(require_auth)])
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

@app.get("/map", dependencies=[Depends(require_auth)])
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

@app.get("/health", dependencies=[Depends(require_auth)])
async def health():

    return {

        "status":
            "online",

        "service":
            "OmnisentryAI",

        "timestamp":
            datetime.utcnow().isoformat()
    }

# ==========================================
# INFO
# ==========================================

@app.get("/info", dependencies=[Depends(require_auth)])
async def info():
    return {
        "name": "Omnisentry AI",
        "description": "AI Website Trust Verification System",
        "version": "0.1.0"
    }

# ==========================================
# CHECK DOMAIN
# ==========================================

@app.get("/check/{domain}", dependencies=[Depends(require_auth)])
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

@app.get("/score/{domain}", dependencies=[Depends(require_auth)])
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

@app.get("/report/{domain}", dependencies=[Depends(require_auth)])
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

@app.get("/report/view/{domain}", dependencies=[Depends(require_auth)])
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

@app.get("/data/{domain}", dependencies=[Depends(require_auth)])
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
@app.get("/omnipop", dependencies=[Depends(require_auth)])
async def omnipop_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="omnipop.html",
        context={
            "request": request
        }
    )
@app.get("/dashboard", dependencies=[Depends(require_auth)])
async def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request
        }
    )


@app.get("/admin")
async def admin_root(request: Request):
    return RedirectResponse(url="/admin/login", status_code=303)

@app.get("/admin/login")
async def admin_login_page(request: Request):
    # If admin already authenticated, send to dashboard
    if request.session.get("admin"):
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse(
        request=request,
        name="admin_login.html",
        context={"request": request},
    )


@app.get("/about", dependencies=[Depends(require_auth)])
async def about_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={
            "request": request
        }
    )


@app.get("/contact", dependencies=[Depends(require_auth)])
async def contact_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="contact.html",
        context={
            "request": request
        }
    )


@app.get("/services", dependencies=[Depends(require_auth)])
async def services_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="services.html",
        context={
            "request": request
        }
    )



# Trust Prediction Route
@app.get("/ai/trust/{domain}", dependencies=[Depends(require_auth)])
async def ai_trust(domain: str):
    report = analyze_website(domain)

    if trust_model is None:
        return {"success": False, "error": "Trust model not loaded"}

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
        "trust_score": report["trust_score"],
        "prediction": int(prediction[0])
    }
#Phishing Detection
@app.get("/ai/phishing", dependencies=[Depends(require_auth)])
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

@app.get("/omnipop/popup/{risk_score}", dependencies=[Depends(require_auth)])
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


@app.get("/omnipop/training-data", dependencies=[Depends(require_auth)])
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



from fastapi import Request

@app.get("/impressum")
def impressum(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="impressum.html",
    )


@app.get("/datenschutz")
def datenschutz(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="datenschutz.html",
    )




from werkzeug.security import generate_password_hash, check_password_hash


# ============================================================
# FASTAPI APPLICATION (Removed duplicate)
# ============================================================
# Using the single FastAPI instance defined above.


# ============================================================



# ============================================================
# JINJA2 TEMPLATES
# ============================================================

# Duplicate Jinja2Templates configuration removed – using the earlier definition (lines 153-155).


# ============================================================
# MOCK DATABASE
users = {}  # in-memory user store
# ============================================================

import uuid
reset_tokens = {}  # in-memory token store





from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware



# ============================================================
# REGISTER - GET
# ============================================================

# ============================================================
# OTP STORAGE
# ============================================================

import random
from datetime import datetime, timedelta

# Temporary in-memory OTP storage
# Later this can be moved to your database.
registration_otps = {}


# ============================================================
# REGISTER - GET
# ============================================================

@app.get("/register")
async def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="registration.html",
        context={
            "request": request
        }
    )

# ============================================================
# SEND OTP - POST
# ============================================================

@app.post("/register/send-otp")
async def send_otp(request: Request, email: str = Form(...)):
    email = email.strip().lower()
    # Generate a 6-digit OTP
    otp = f"{random.randint(0, 999999):06d}"
    expires = datetime.now(timezone.utc) + timedelta(minutes=5)
    # Store OTP with expiration
    registration_otps[email] = {"otp": otp, "expires": expires}
    # Send OTP via email if mail is configured
    if fastmail:
        try:
            message = MessageSchema(
                subject="Your verification code",
                recipients=[email],
                body=f"Your OTP code is {otp}. It expires in 5 minutes.",
                subtype=MessageType.plain,
            )
            await fastmail.send_message(message)
        except Exception as e:
            # Log the error and continue; display OTP for debugging
            print(f"Email send failed: {e}")
            return templates.TemplateResponse(
                request=request,
                name="registration.html",
                context={
                    "request": request,
                    "email": email,
                    "error": "Failed to send OTP email. Use the code displayed here.",
                    "success": f"Your OTP is {otp}. (Email delivery failed)"
                },
                status_code=200
            )
    # Return success response
    return templates.TemplateResponse(
        request=request,
        name="registration.html",
        context={
            "request": request,
            "email": email,
            "success": f"Verification code sent to {email}."
        },
        status_code=200
    )
# ============================================================
# REGISTER - POST
# ============================================================

@app.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(None),
    otp: str = Form(None)
):

    email = email.strip().lower()
    otp = (otp or "").strip()

    # ------------------------------------------
    # Validate email
    # ------------------------------------------

    if not email:

        return templates.TemplateResponse(
            request=request,
            name="registration.html",
            context={
                "request": request,
                "error": "Email address is required."
            },
            status_code=400
        )

    # ------------------------------------------
    # Validate password length
    # ------------------------------------------

    if len(password) < 8:

        return templates.TemplateResponse(
            request=request,
            name="registration.html",
            context={
                "request": request,
                "email": email,
                "error": (
                    "Password must contain at least "
                    "8 characters."
                )
            },
            status_code=400
        )

    # ------------------------------------------
    # Confirm passwords
    # ------------------------------------------

    if not confirm_password:
            return templates.TemplateResponse(
                request=request,
                name="registration.html",
                context={
                    "request": request,
                    "email": email,
                    "error": "Confirm password is required."
                },
                status_code=400
            )

    if password != confirm_password:
            return templates.TemplateResponse(
                request=request,
                name="registration.html",
                context={
                    "request": request,
                    "email": email,
                    "error": "Passwords do not match."
                },
                status_code=400
            )

    # ------------------------------------------
    # Validate OTP format
    # ------------------------------------------

    if not otp.isdigit() or len(otp) != 6:

        return templates.TemplateResponse(
            request=request,
            name="registration.html",
            context={
                "request": request,
                "email": email,
                "error": (
                    "Please enter a valid "
                    "6-digit verification code."
                )
            },
            status_code=400
        )

    # ------------------------------------------
    # Get stored OTP
    # ------------------------------------------

    otp_data = registration_otps.get(email)

    if not otp_data:

        return templates.TemplateResponse(
            request=request,
            name="registration.html",
            context={
                "request": request,
                "email": email,
                "error": (
                    "No verification code was found. "
                    "Please request a new OTP."
                )
            },
            status_code=400
        )

    # ------------------------------------------
    # Check OTP expiration
    # ------------------------------------------

    now = datetime.now(timezone.utc)

    if now > otp_data["expires"]:

        registration_otps.pop(
            email,
            None
        )

        return templates.TemplateResponse(
            request=request,
            name="registration.html",
            context={
                "request": request,
                "email": email,
                "error": (
                    "Your verification code has "
                    "expired. Please request a new one."
                )
            },
            status_code=400
        )

    # ------------------------------------------
    # Check OTP
    # ------------------------------------------

    if not secrets.compare_digest(
        otp,
        otp_data["otp"]
    ):

        return templates.TemplateResponse(
            request=request,
            name="registration.html",
            context={
                "request": request,
                "email": email,
                "error": (
                    "The verification code "
                    "is incorrect."
                )
            },
            status_code=400
        )

    # ------------------------------------------
    # Check duplicate account
    # ------------------------------------------

    for user_data in users.values():

        if not isinstance(user_data, dict):
            continue

        existing_email = user_data.get(
            "email",
            ""
        ).strip().lower()

        if existing_email == email:

            return templates.TemplateResponse(
                request=request,
                name="registration.html",
                context={
                    "request": request,
                    "email": email,
                    "error": (
                        "An account with this email "
                        "already exists."
                    )
                },
                status_code=400
            )

    # ------------------------------------------
    # Hash password
    # ------------------------------------------

    hashed_password = generate_password_hash(
        password,
        method="pbkdf2:sha256"
    )

    # ------------------------------------------
    # Create Viewer account
    # ------------------------------------------

    users[email] = {
        "email": email,
        "password": hashed_password,
        "role": "viewer",
        "email_verified": True,
        "created_at": (
            datetime.now(timezone.utc).isoformat()
        )
    }

    # ------------------------------------------
    # Delete OTP after successful use
    # ------------------------------------------

    registration_otps.pop(
        email,
        None
    )

    # ------------------------------------------
    # Redirect to login
    # ------------------------------------------

    return RedirectResponse(
        url="/login",
        status_code=303
    )

# ============================================================
# LOGIN - GET
# ============================================================

@app.get("/login", response_class=HTMLResponse)

async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"show_register": request.query_params.get('show') == 'register'}
    )

# ============================================================
# LOGIN - POST
# ============================================================

@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):

    # Find user by email
    user_data = users.get(email)
    if user_data:
        user_password = user_data.get("password")
    else:
        user_password = None

    if not user_password or not check_password_hash(
        user_password,
        password
    ):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"request": request},
            status_code=200,
        )

    # Store username in session
    request.session["username"] = email

    # Redirect to dashboard
    return RedirectResponse(url="/dashboard", status_code=303)

# ============================================================
# FORGOT PASSWORD - GET
# ============================================================

@app.get("/forgot_password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="forgot_password.html",
        context={"request": request}
    )

# ============================================================
# FORGOT PASSWORD - POST
# ============================================================




# ============================================================
# FORGOT PASSWORD - POST
# ============================================================

@app.post("/forgot_password")
async def forgot_password(
    request: Request,
    username: str = Form(...)
):
    # Get user data
    user_data = users.get(username)

    # Do not reveal whether the account exists
    if not user_data:
        return templates.TemplateResponse(
            request=request,
            name="forgot_password.html",
            context={
                "request": request,
                "message": (
                    "If the username exists, "
                    "a reset link has been sent."
                )
            },
            status_code=200,
        )

    # Get registered email address
    user_email = user_data.get("email")

    if not user_email:
        return templates.TemplateResponse(
            request=request,
            name="forgot_password.html",
            context={
                "request": request,
                "error": "No email address is associated with this account."
            },
            status_code=400,
        )

    # Generate secure reset token
    token = str(uuid.uuid4())

    # Store token with expiration time
    reset_tokens[token] = {
        "username": username,
        "expires": datetime.utcnow() + timedelta(hours=1)
    }

    # Generate password reset URL
    reset_link = str(
        request.url_for(
            "reset_password_page",
            token=token
        )
    )

    # Email body
    email_body = f"""
    <h2>Omminsentiry AI Password Reset</h2>

    <p>Hello {username},</p>

    <p>
        We received a request to reset the password
        for your Omminsentiry AI account.
    </p>

    <p>
        Click the link below to create a new password:
    </p>

    <p>
        <a href="{reset_link}">
            Reset Password
        </a>
    </p>

    <p>
        This password-reset link expires in 1 hour.
    </p>

    <p>
        If you did not request a password reset,
        you can ignore this email.
    </p>

    <p>
        Omminsentiry AI Security Team
    </p>
    """

    # Create email
    message = MessageSchema(
        subject="Reset Your Omminsentiry AI Password",
        recipients=[user_email],
        body=email_body,
        subtype=MessageType.html,
    )

    # Send email
    try:
        await fastmail.send_message(message)

    except Exception as e:
        print(f"Password reset email error: {e}")

        return templates.TemplateResponse(
            request=request,
            name="forgot_password.html",
            context={
                "request": request,
                "error": "Unable to send the reset email. Please try again."
            },
            status_code=500,
        )

    # Confirmation page
    return templates.TemplateResponse(
        request=request,
        name="reset_password_sent.html",
        context={
            "request": request,
            "message": (
                "If the username exists, "
                "a password reset link has been sent."
            )
        }
    )


# ============================================================
# RESET PASSWORD - GET
# ============================================================

@app.get("/reset_password/{token}", response_class=HTMLResponse, name="reset_password_page")
async def reset_password_page(request: Request, token: str):
    token_data = reset_tokens.get(token)
    if not token_data or token_data["expires"] < datetime.utcnow():
        return templates.TemplateResponse(
            "reset_password.html",
            {"request": request, "error": "Invalid or expired token."},
            status_code=400,
        )
    return templates.TemplateResponse(
        request=request,
        name="reset_password.html",
        context={"request": request, "token": token}
    )

# ============================================================
# RESET PASSWORD - POST
# ============================================================

@app.post("/reset_password/{token}")
async def reset_password(request: Request, token: str, password: str = Form(...), confirm: str = Form(...)):
    token_data = reset_tokens.get(token)
    if not token_data or token_data["expires"] < datetime.utcnow():
        return templates.TemplateResponse(
            "reset_password.html",
            {"request": request, "error": "Invalid or expired token."},
            status_code=400,
        )
    if password != confirm:
        return templates.TemplateResponse(
            "reset_password.html",
            {"request": request, "token": token, "error": "Passwords do not match."},
            status_code=200,
        )
    # Update user's password
    username = token_data["username"]
    users[username] = generate_password_hash(password, method="pbkdf2:sha256")
    # Remove token
    del reset_tokens[token]
    # Redirect to login
    return RedirectResponse(url="/login", status_code=303)

# ============================================================
# DASHBOARD
# ============================================================

@app.get(
    "/dashboard",
    response_class=HTMLResponse,
    dependencies=[Depends(require_auth)]
)
async def dashboard(request: Request):

    username = request.session.get("username")

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "username": username
        }
    )


# ============================================================
# LOGOUT
# ============================================================

@app.get("/logout")
async def logout(request: Request):

    # Clear the authenticated session
    request.session.clear()

    # Redirect to login
    return RedirectResponse(
        url="/login",
        status_code=303
    )


@app.get("/password-reset-sent", response_class=HTMLResponse)
async def password_reset_sent(request: Request, reset_link: str):
    return templates.TemplateResponse(
        "password_reset_sent.html",
        {
            "request": request,
            "reset_link": reset_link,
        },
    )



# ============================================================
# HOME
# ============================================================

@app.get("/")
async def home():

    return RedirectResponse(
        url="/login",
        status_code=303
    )

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



