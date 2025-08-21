📦 CloudFile_Storage

A FastAPI project that provides secure file upload, download, listing, and deletion using Azure Blob Storage, with OTP-based login and JWT authentication.

🚀 Features

🔐 OTP-based email authentication (Azure Communication Services or dev fallback)

🔑 JWT-secured endpoints

📂 Upload files to Azure Blob Storage

📥 Download files securely

🗑️ Delete files

📜 List uploaded files with metadata

🌍 CORS restricted for security

🛠️ Tech Stack

FastAPI

Azure Blob Storage

Azure Communication Services
 (for OTP via email)

JWT Authentication

Python 3.9+

⚙️ Setup & Installation
1️⃣ Clone the repo
git clone https://github.com/<your-username>/CloudFile_Storage.git
cd CloudFile_Storage

2️⃣ Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Configure environment variables

Create a .env file in the root folder:

AZURE_CONNECTION_STRING="your-azure-blob-connection-string"
CONTAINER_NAME="your-container-name"
JWT_SECRET="super-secret-random-string"
JWT_ISSUER="cloudbox"
JWT_EXPIRE_MIN=60
OTP_EXPIRE_MIN=5
ACS_CONNECTION_STRING="your-acs-connection-string"
ACS_EMAIL_SENDER="DoNotReply@xxxx.azurecomm.net"

5️⃣ Run the server
uvicorn main:app --reload


Server will run at: http://127.0.0.1:8000

📌 API Endpoints
🔑 Auth

POST /auth/request-otp → Request OTP

POST /auth/verify-otp → Verify OTP and receive JWT

📂 Files

POST /upload → Upload a file (JWT required)

GET /files → List all files (JWT required)

GET /download/{filename} → Download a file (JWT required)

DELETE /delete/{filename} → Delete a file (JWT required)

🔒 Authentication

All file operations require a JWT token in the header:

Authorization: Bearer <your_token>
