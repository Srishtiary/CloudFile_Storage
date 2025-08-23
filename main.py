from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Header
from azure.storage.blob import BlobServiceClient
from fastapi import Response
from backend.config import (
    AZURE_CONNECTION_STRING, CONTAINER_NAME,
    ACS_CONNECTION_STRING, ACS_EMAIL_SENDER,
    JWT_SECRET, JWT_ISSUER, JWT_EXPIRE_MIN, OTP_EXPIRE_MIN
)
from typing import Optional
from datetime import datetime, timedelta, timezone
import re, random, string, jwt, os

DEV_MODE = os.getenv("DEV_MODE", "0") == "1"  # <— optional: dev OTP fallback

# ---- ACS Clients ----
try:
    from azure.communication.email import EmailClient
    email_client = EmailClient.from_connection_string(ACS_CONNECTION_STRING) if ACS_EMAIL_SENDER else None
except Exception:
    email_client = None

app = FastAPI()

# Azure Blob client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)
try:
    container_client.create_container()
except Exception:
    pass

@app.get("/")
def root():
    return {"message": "FastAPI Azure Blob Storage API running"}

# ======== OTP Store ========
OTP_STORE = {}

def generate_otp(n=6) -> str:
    return "".join(random.choices(string.digits, k=n))

def is_email(s: str) -> bool:
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", s) is not None

def send_otp_via_email(to_email: str, otp: str):
    if not email_client or not ACS_EMAIL_SENDER:
        raise RuntimeError("Email not configured.")
    poller = email_client.begin_send({
        "content": {
            "subject": "Your Cloud Box OTP",
            "plainText": f"Your OTP is: {otp}. It expires in {OTP_EXPIRE_MIN} minutes."
        },
        "recipients": {"to": [{"address": to_email}]},
        "senderAddress": ACS_EMAIL_SENDER
    })
    poller.result()  # Wait for send to complete

@app.post("/auth/request-otp")
async def request_otp(payload: dict):
    contact = (payload.get("contact") or "").strip()
    if not contact or not is_email(contact):
        raise HTTPException(status_code=400, detail="Provide a valid email address.")

    code = generate_otp()
    OTP_STORE[contact] = {
        "otp": code,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=OTP_EXPIRE_MIN)
    }
    # DEV fallback
    if DEV_MODE:
        print(f"[DEV OTP] {contact} -> {code}")
        return {"message": "OTP generated (DEV_MODE). Check server logs."}


    try:
        send_otp_via_email(contact, code)
    except Exception as e:
        OTP_STORE.pop(contact, None)
        raise HTTPException(status_code=500, detail=f"Failed to send OTP: {e}")

    return {"message": "OTP sent"}

def create_jwt(sub: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "iss": JWT_ISSUER,
        "sub": sub,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=JWT_EXPIRE_MIN)).timestamp())
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

@app.post("/auth/verify-otp")
async def verify_otp(payload: dict):
    contact = (payload.get("contact") or "").strip()
    otp = (payload.get("otp") or "").strip()

    rec = OTP_STORE.get(contact)
    if not rec or rec["otp"] != otp or rec["exp"] < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP.")

    OTP_STORE.pop(contact, None)
    token = create_jwt(contact)
    return {"token": token}

# ======== JWT Dependency ========
def require_auth(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token.")
    token = authorization.split(" ", 1)[1].strip()
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"], options={"require": ["exp", "sub"]})
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired.")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token.")
    return decoded

# ======== Protected Upload ========
@app.post("/upload")
async def upload_file(file: UploadFile = File(...), user=Depends(require_auth)):
    try:
        blob_client = container_client.get_blob_client(file.filename)
        file_data = await file.read()
        blob_client.upload_blob(file_data, overwrite=True)
        return {"message": "File uploaded successfully", "blob_url": blob_client.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ======== List Files ========
@app.get("/files")
async def list_files(user=Depends(require_auth)):
    try:
        blobs = container_client.list_blobs()
        files = []
        for blob in blobs:
            files.append({
                "name": blob.name,
                "size": blob.size,
                "last_modified": blob.last_modified.isoformat(),
                "url": container_client.get_blob_client(blob).url
            })
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str, user=Depends(require_auth)):
    try:
        blob_client = container_client.get_blob_client(filename)
        stream = blob_client.download_blob()
        return Response(
            content=stream.readall(),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"File not found: {e}")

@app.delete("/delete/{filename}")
async def delete_file(filename: str, user=Depends(require_auth)):
    try:
        blob_client = container_client.get_blob_client(filename)
        blob_client.delete_blob()
        return {"message": f"{filename} deleted successfully"}
    except Exception as e:

        raise HTTPException(status_code=404, detail=f"File not found or cannot delete: {e}")
