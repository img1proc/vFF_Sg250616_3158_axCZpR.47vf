from flask import Flask, render_template, request
import os, tempfile

from utils.verify_signature import verify_signature

app = Flask(__name__)
UPLOAD_FOLDER = tempfile.gettempdir()

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    hash_value = None
    error = None

    if request.method == "POST":
        try:
            pdf_file = request.files["pdf"]
            sig_file = request.files["signature"]
            pubkey_file = request.files["public_key"]

            pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
            sig_path = os.path.join(UPLOAD_FOLDER, sig_file.filename)
            pubkey_path = os.path.join(UPLOAD_FOLDER, pubkey_file.filename)

            pdf_file.save(pdf_path)
            sig_file.save(sig_path)
            pubkey_file.save(pubkey_path)

            is_valid, info = verify_signature(pdf_path, sig_path, pubkey_path)

            if is_valid:
                result = "✅ Signature Verified"
                hash_value = info
            else:
                result = "❌ Signature does NOT match"
                error = info

        except Exception as e:
            error = str(e)

    return render_template("index.html", result=result, hash_value=hash_value, error=error)