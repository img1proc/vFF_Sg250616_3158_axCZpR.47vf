from flask import Flask, render_template, request, send_file, redirect
import os
import tempfile
from utils.verify_signature import verify_signature

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

@app.route('/', methods=['GET', 'POST'])
def verify():
    result = None
    error = None
    hash_original = None
    hash_decrypted = None

    if request.method == 'POST':
        pdf = request.files.get('pdf')
        signature = request.files.get('signature')
        public_key = request.files.get('public_key')

        if not pdf or not signature or not public_key:
            error = 'All three files are required.'
        else:
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf.filename)
            sig_path = os.path.join(app.config['UPLOAD_FOLDER'], signature.filename)
            pub_path = os.path.join(app.config['UPLOAD_FOLDER'], public_key.filename)

            pdf.save(pdf_path)
            signature.save(sig_path)
            public_key.save(pub_path)

            try:
                match, hash_original, hash_decrypted = verify_signature(pdf_path, sig_path, pub_path)
                result = '✔️ Signature Verified' if match else '❌ Signature does NOT match'
            except Exception as e:
                error = f'Error verifying signature: {str(e)}'

    return render_template('verify.html',
                           result=result,
                           error=error,
                           hash_original=hash_original,
                           hash_decrypted=hash_decrypted)