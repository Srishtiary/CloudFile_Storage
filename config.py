import os
from dotenv import load_dotenv
load_dotenv()

AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("CONTAINER_NAME", "uploads")

# OTP / Auth config
JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ISSUER = os.getenv("JWT_ISSUER", "cloudbox")
JWT_EXPIRE_MIN = int(os.getenv("JWT_EXPIRE_MIN", "60"))
OTP_EXPIRE_MIN = int(os.getenv("OTP_EXPIRE_MIN", "5"))

# Azure Communication Services (Email or SMS)
ACS_CONNECTION_STRING = os.getenv("ACS_CONNECTION_STRING")
ACS_EMAIL_SENDER = os.getenv("ACS_EMAIL_SENDER")
ACS_SMS_SENDER = os.getenv("ACS_SMS_SENDER")
