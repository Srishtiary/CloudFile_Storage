📦 CloudFile_Storage
A FastAPI project that provides secure file upload, download, listing, and deletion using Azure Blob Storage, with OTP-based login and JWT authentication.

FastAPI Azure Blob Storage API 🚀
This project is a FastAPI-based REST API that allows users to:

🔑 Authenticate with OTP (One Time Password)
📤 Upload files to Azure Blob Storage
📥 Download files
❌ Delete files
✅ Verify OTP with JWT authentication

🔧 Features
User authentication with JWT (Bearer Token)
File storage in Azure Blob Storage
Endpoints to upload, download, list, and delete files
Postman collection for testing

📦 Requirements
Python 3.9+
FastAPI
Uvicorn
Azure Storage Blob SDK
Install dependencies: pip install fastapi uvicorn python-multipart azure-storage-blob python-jose

▶️Run the Project
Start the FastAPI server:
uvicorn main:app --reload
The API will be available at:
http://127.0.0.1:8000

🔑Authentication Flow
Request OTP → /auth/request-otp
Verify OTP → /auth/verify-otp → receive JWT token
Use the token in Authorization Header for all requests:
Authorization: Bearer <your_token>

📂API Endpoints
1. Request OTP :-POST /auth/request-otp
2. Verify OTP :- POST /auth/verify-otp
3. Upload File:- POST /upload
Headers: Authorization: Bearer <token>
Body:form-data → file=<your_file>
4. Download File:-DELETE /delete/{filename}
Headers: Authorization: Bearer <token>

📝 Notes
Make sure you configure your Azure Blob Storage credentials inside your project (connection_string, container_name).
Don’t upload secrets (like connection strings or tokens) to GitHub. Use .env files or GitHub Secrets.
