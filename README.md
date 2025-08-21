📦 CloudFile_Storage

A FastAPI project that provides secure file upload, download, listing, and deletion using Azure Blob Storage, with OTP-based login and JWT authentication.

🚀 Features

🔐 Authenticate with OTP (One Time Password)

🔑 Verify OTP with JWT authentication

📂 Upload files to Azure Blob Storage

📥 Download files securely

🗑️ Delete files

🛠️ Requirements

Python 3.9+

FastAPI

Uvicorn

Azure Storage Blob SDK

python-jose

Install dependencies:

pip install fastapi uvicorn azure-storage-blob python-multipart python-jose

▶️ Run the Project

Start the FastAPI server:

uvicorn main:app --reload


The API will be available at:
👉 http://127.0.0.1:8000

🔑 Authentication Flow

Request OTP → POST /auth/request-otp

Verify OTP → POST /auth/verify-otp → receive JWT token

Use token in header for all requests:

Authorization: Bearer <your_token>

📂 API Endpoints
🔑 Auth

POST /auth/request-otp → Request OTP

POST /auth/verify-otp → Verify OTP and get JWT

📂 Files

POST /upload → Upload file

Headers: Authorization: Bearer <token>

Body: form-data → file=<your_file>

GET /files → List all files

GET /download/{filename} → Download file

DELETE /delete/{filename} → Delete file

⚠️ Notes

Configure your Azure Blob Storage credentials in .env (connection string, container name).

Do NOT upload secrets (connection strings, tokens) to GitHub.

Use .env files or GitHub Secrets.
