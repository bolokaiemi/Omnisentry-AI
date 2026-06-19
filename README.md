# 🛡️ Omnisentry AI Trust Verification

## 📌 Overview

Omnisentry AI is an AI-powered website trust verification system designed to help users stay safe online.

It works as an intelligent security layer that analyzes websites in real time and provides trust insights before users interact with them.

The system functions like a browser-based security assistant, inspecting domains, security signals, registration data, and reputation indicators to help detect potential threats such as phishing, scams, fraud, malware, and unsafe websites.

---

## ⚙️ Core Functionality

### 🔍 Website Analysis

* Scans domain information automatically
* Checks domain age and registration status
* Evaluates SSL/HTTPS security status
* Analyzes website reputation signals
* Reviews trust indicators and security factors

### 🧠 AI Trust Scoring

* Generates a trust score (0–100)
* Uses AI-assisted evaluation techniques
* Classifies websites into risk levels:

#### Risk Levels

* 🟢 Safe
* 🟡 Medium Risk
* 🟠 High Risk
* 🔴 Critical Risk

### 🌐 Security Intelligence

* Detects suspicious or unverified websites
* Identifies missing or invalid SSL certificates
* Flags potentially malicious domains
* Monitors trust indicators for suspicious activity

### 🚨 Security Alerts

* Warns users against sharing financial information on unverified sites
* Warns users against sharing personal information on suspicious websites
* Provides real-time risk notifications before user interaction
* Helps prevent phishing and fraud attempts

---

## 🧩 System Features

* AI-powered trust evaluation engine
* Domain verification system
* SSL and HTTPS validation
* Reputation and threat scoring
* Website trust assessment
* Browser-style security interface (pop-up concept)
* Modular architecture for future expansion
* Optional location/IP-based analysis

---

## 🛠️ Done So Far (Mobile Connected Security Ecosystem Integration)

We have successfully migrated Omminsentiry AI from a website-only service into a full mobile-connected security ecosystem (App Store app + OmniRover + Backend). The following items are completed:

1. **Ecosystem Cleanup**: Merged and consolidated the malformed ` omnirover` folder into the clean python package directory `omnirover/`, resolving Python package import issues.
2. **Upgraded Relational Database Setup**: Expanded the schemas in `database/init_db.py` to support mobile device registration, platform tracking, live status, configurations (Parental Control, Payment Guard toggles), threat logging, and incident alerts linked directly to specific devices.
3. **Mobile Client Agent (`omnirover`)**: Implemented the client-side pipeline to scan page content, execute payment guard and parental checks, encrypt data payloads, and securely post threat telemetry to the backend. Includes an in-process fallback mechanism to support testing when the backend server is run in-process.
4. **Backend Event & Storage Layer**: Built services under `backend/` for managing devices, logging domain scans, generating critical alerts for scores $\ge 70$, logging mock push notifications, and dispatching security events to a Security Operations Center log.
5. **FastAPI Route Mapping**: Created routes in `backend/api_routes.py` (mounted in `app.py`) exposing telemetry reports, config sync, registration, metrics, and simulation trigger endpoints.
6. **Mobile Sandbox Permissions Profile**: Loaded and cleaned `mobile_app/permissions.json` to configure app permissions dynamically.
7. **Security Dashboard UI Overhaul**: Created a gorgeous, glassmorphic security center dashboard that queries live database statistics, displays registered mobile devices with platform badges, streams incident alerts, and includes a **Mobile Threat Simulation Controller** to execute simulated mobile scans directly from the browser.
8. **Automated Testing Suite**: Corrected unit test assertion errors and imports. All 42 unit tests pass successfully, and E2E integration verification script runs completely green.

---

## 🚀 How It Works

### Step 1

User enters a website domain.

Example:
google.com
...text
### Step 2
...

The system performs security checks:

* Domain registration analysis
* Domain age verification
* SSL certificate validation
* Reputation assessment
* Trust indicator evaluation

### Step 3

The AI engine calculates a trust score.

Example:

```text
Trust Score: 87/100
```

### Step 4

The system generates a structured security report.

### Step 5

The user interface displays:

* Trust score
* SSL status
* Domain information
* Reputation indicators
* Security warnings

---

## 🔐 Goal of the Project

To build a real-time AI security layer for the web that helps users:

* Avoid phishing attacks
* Identify unsafe websites
* Reduce exposure to scams
* Make safer browsing decisions
* Understand website trustworthiness instantly
* Improve online security awareness

---

## 📈 Future Improvements

### Browser Extension

* Live browser extension version for real-time website protection
* Automatic trust verification while browsing

### Threat Intelligence

* Integration with global phishing databases
* Integration with malware and threat intelligence feeds
* Automated scam detection updates

### Geolocation & Mapping

* Geo-location based risk mapping
* IP intelligence and location analysis
* Interactive security map visualization

### Advanced AI Security

* Advanced AI anomaly detection
* Behavioral website analysis
* Machine learning threat prediction
* Enhanced trust classification models

### Enterprise Features

* Enterprise-grade security API
* Security dashboard and reporting
* Multi-user monitoring platform

### Active Threat Intelligence Module

A background threat intelligence system that continuously queries trusted security sources to detect:

* Emerging scam domains
* Phishing campaigns
* Malicious actors
* Fraudulent websites
* Newly discovered threats

The collected intelligence is fed back into the Omminsentiry AI trust verification engine to improve future security assessments and risk detection.

---

## 🛠️ Technology Stack

### Backend

* FastAPI
* Python
* Jinja2
* Uvicorn

### Machine Learning

* Scikit-learn
* Pandas
* Pickle

### Frontend

* HTML5
* CSS3
* JavaScript

---

## ⚠️ Disclaimer

Omnisentry AI provides security assessments and risk estimations based on available information and analysis techniques.

The platform does not guarantee that a website is completely safe or completely malicious.

Users should always exercise caution when:

* Sharing personal information
* Entering financial details
* Downloading files
* Installing software
* Making online payments

Final security decisions remain the responsibility of the user.

---

## 📄 License

This project is now completed and no longer under development.

Copyright © 2026, Ebi Emmeric-Adehor.
All rights reserved.
