echo "# 🌩️ Cloud File Storage with Flask & Azure Blob

This is a cloud-based file storage web app built with Flask and integrated with Azure Blob Storage. Users can sign in, upload files, and store them securely in the cloud.

## 📦 Features
- HTML/CSS frontend with modern UI
- Login form with email/password input
- Upload files directly to Azure Blob Storage
- Success message & link to uploaded file (hidden on frontend)
- Python Flask backend for handling file requests

## 🧰 Tech Stack
- Python 3
- Flask
- Azure Blob Storage
- HTML, CSS, JavaScript
- Git & GitHub

## ⚙️ How to Run Locally

\`\`\`bash
git clone https://github.com/Shrishtiarya/CloudFile_Storage.git
cd CloudFile_Storage
pip install -r requirements.txt
python app.py
\`\`\`

App will run locally on: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 📁 Project Structure

\`\`\`
CloudFile_Storage/
│
├── app.py
├── requirements.txt
├── templates/
│   ├── index.html
│   ├── signin.html
│   └── dashboard.html
└── static/ (optional for assets)
\`\`\`

## ☁️ Cloud Integration
- Uses Azure Blob Storage SDK to upload and manage files
- Stores uploaded blobs in the 'datastorage' container
- Azure Connection String is securely managed

## 🚀 Status
✅ Project Completed  
✅ Successfully Pushed to GitHub  
🔜 Ready for Deployment (e.g., Azure App Service)

---

"Cloud storage made simple with Flask and Azure."
"Developed by Shrishti Arya 💻☁️"
"🔗 https://github.com/Shrishtiarya/CloudFile_Storage"
""> README.md

git add README.md
git commit -m "Add README"
git push
