from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import json

from backend.device_manager import register_device, update_device_status, get_devices
from backend.event_store import store_report, get_recent_reports, get_stats, get_recent_threat_logs
from backend.alert_engine import process_report_for_alerts, get_recent_alerts
from backend.feedback_store import add_feedback, get_all_feedback, get_milestone_metrics
from omnirover.encrypted_channel import decrypt_data
from omnirover.rover_core import OmniRover

router = APIRouter(prefix="/api")


# Models for Request Payloads
class RegisterPayload(BaseModel):
    device_id: str
    platform: str

class StatusPayload(BaseModel):
    device_id: str
    settings: dict

class ReportPayload(BaseModel):
    encrypted_payload: str
    device_id: str

class SimulatePayload(BaseModel):
    device_id: str
    platform: str
    domain: str
    page_content: str

# 1. Device Endpoints
@router.post("/device/register")
async def api_register_device(payload: RegisterPayload):
    success = register_device(payload.device_id, payload.platform)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to register device")
    return {"status": "success", "message": f"Device {payload.device_id} registered"}

@router.post("/device/status")
async def api_update_device_status(payload: StatusPayload):
    success = update_device_status(payload.device_id, payload.settings)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update device status")
    return {"status": "success", "message": f"Device {payload.device_id} status updated"}

# 2. Threat Telemetry Endpoint
@router.post("/threat/report")
async def api_threat_report(payload: ReportPayload, background_tasks: BackgroundTasks):
    try:
        decrypted = decrypt_data(payload.encrypted_payload)
        data = json.loads(decrypted)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to decrypt payload: {str(e)}")
        
    report = data.get("report", {})
    domain = report.get("domain", "unknown.com")
    risk_score = report.get("risk_score", 0)
    
    # Store report in database
    store_report(
        device_id=payload.device_id,
        domain=domain,
        risk_score=risk_score,
        status="FLAGGED" if risk_score >= 50 else "CLEAN",
        threats=report.get("threats", {}).get("detected", []),
        timestamp=data.get("timestamp")
    )
    
    # Run alert checks in background to keep API responsive
    background_tasks.add_task(process_report_for_alerts, payload.device_id, report)
    
    return {"status": "success", "message": "Telemetry received and logged"}

# 3. Dashboard Endpoints
@router.get("/dashboard/stats")
async def api_dashboard_stats():
    return get_stats()

@router.get("/dashboard/devices")
async def api_dashboard_devices():
    return get_devices()

@router.get("/dashboard/threats")
async def api_dashboard_threats():
    # Returns recent scans/reports
    return get_recent_reports(limit=15)

@router.get("/dashboard/alerts")
async def api_dashboard_alerts():
    return get_recent_alerts(limit=15)

# 4. Pipeline Simulator Endpoint
@router.post("/simulator/trigger")
async def api_simulator_trigger(payload: SimulatePayload, background_tasks: BackgroundTasks):
    # Register the device first
    register_device(payload.device_id, payload.platform)
    
    # Instantiate the rover with custom endpoint for loopback simulation
    rover = OmniRover(
        device_id=payload.device_id,
        platform=payload.platform,
        backend_url="http://127.0.0.1:8000"
    )
    
    # Execute the scan (automatically sends the report to /api/threat/report if risk > 30)
    scan_result = rover.scan(payload.page_content, domain=payload.domain)
    
    # If the risk score was low (< 30) and didn't auto-send, we force log it as a report
    # so that the user sees the scan in the dashboard reports table anyway
    if scan_result["risk_score"] <= 30:
        store_report(
            device_id=payload.device_id,
            domain=payload.domain,
            risk_score=scan_result["risk_score"],
            status="CLEAN",
            threats=[],
            timestamp=None
        )
        
    return {
        "status": "success",
        "message": f"Simulation executed for {payload.domain}",
        "scan_result": scan_result
    }

# 5. Mobile Permissions Endpoint
@router.get("/app/permissions")
async def api_app_permissions():
    try:
        with open("mobile_app/permissions.json", "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read permissions: {str(e)}")

# 6. Pre-Registration Feedback & Milestones Endpoints
class FeedbackPayload(BaseModel):
    name: str
    rating: int
    comment: str

@router.get("/feedback")
async def api_get_feedback():
    return get_all_feedback()

@router.post("/feedback")
async def api_add_feedback(payload: FeedbackPayload):
    if not payload.name.strip() or not payload.comment.strip() or not (1 <= payload.rating <= 5):
        raise HTTPException(status_code=400, detail="Invalid review fields.")
    success = add_feedback(payload.name.strip(), payload.rating, payload.comment.strip())
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save feedback.")
    return {"status": "success", "message": "Feedback submitted successfully."}

@router.get("/milestone")
async def api_get_milestone():
    return get_milestone_metrics()


class AdminVerifyPayload(BaseModel):
    password: str

@router.post("/admin/verify")
async def api_verify_admin(payload: AdminVerifyPayload):
    import os
    correct_password = os.getenv("ADMIN_PASSWORD", "admin123")
    if payload.password == correct_password:
        return {"status": "success", "message": "Admin verified successfully."}
    raise HTTPException(status_code=401, detail="Incorrect admin password.")



