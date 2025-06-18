from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from hashlib import sha256

def verify_signature(pdf_path, signature_path, public_key_path):
    try:
        # PDFを読み込んでSHA-256ハッシュを計算
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
        hash_value = sha256(pdf_data).digest()

        # 署名を読み込み
        with open(signature_path, "rb") as f:
            signature = f.read()

        # 公開鍵を読み込み
        with open(public_key_path, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())

        # 検証
        public_key.verify(
            signature,
            hash_value,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        return True, hash_value.hex()

    except InvalidSignature:
        return False, "Signature does NOT match"
    except Exception as e:
        return False, str(e)