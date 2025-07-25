from flask import Flask, request, jsonify
from azure.storage.blob import BlobServiceClient
import os
from flask import render_template


app = Flask(__name__)

AZURE_CONNECTION_STRING = "Connection String"
CONTAINER_NAME = "datastorage"

blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

container_client = blob_service_client.get_container_client(CONTAINER_NAME)
try:
    container_client.create_container()
    print(f"Container '{CONTAINER_NAME}' created.")
except Exception:
    print(f"Container '{CONTAINER_NAME}' already exists.")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        # You can add real auth logic here later
        print(f"User signed in with: {email} / {password}")
        return render_template("dashboard.html")
    else:
        return "Invalid access. Please sign in through the login form.", 400

#@app.route("/")
#def hello():
#    return "Hello world!"

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        blob_client = container_client.get_blob_client(file.filename)

        blob_client.upload_blob(file.read(), overwrite=True)

        blob_url = blob_client.url

        return jsonify({"message": "File uploaded successfully", "blob_url": blob_url}), 200

    except Exception as e:
        return jsonify({"error": f"{type(e).__name__}: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)