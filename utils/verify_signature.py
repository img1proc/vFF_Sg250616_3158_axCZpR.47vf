import subprocess

def verify_signature(pdf_path, sig_path, pub_key_path):
    try:
        # OpenSSLコマンドで署名の検証を実行
        result = subprocess.run([
            'openssl', 'dgst', '-sha256',
            '-verify', pub_key_path,
            '-signature', sig_path,
            pdf_path
        ], check=True, stderr=subprocess.PIPE)

        return True, "Match", "Match"

    except subprocess.CalledProcessError as e:
        # 検証失敗（署名が一致しない、鍵エラーなど）
        return False, "Verification Failed", e.stderr.decode().strip()