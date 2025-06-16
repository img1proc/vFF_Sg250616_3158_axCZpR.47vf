import hashlib
import subprocess

def verify_signature(pdf_path, sig_path, pub_key_path):
    # PDFのハッシュを計算
    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()
        pdf_hash = hashlib.sha256(pdf_data).hexdigest()

    # 署名ファイルを公開鍵で復号
    decrypted_path = sig_path + '.decrypted.txt'

    subprocess.run([
        'openssl', 'rsautl', '-verify',
        '-inkey', pub_key_path,
        '-pubin',
        '-in', sig_path,
        '-out', decrypted_path
    ], check=True)

    with open(decrypted_path, 'rb') as f:
        decrypted_hash = f.read().hex()

    match = (pdf_hash == decrypted_hash)
    return match, pdf_hash, decrypted_hash