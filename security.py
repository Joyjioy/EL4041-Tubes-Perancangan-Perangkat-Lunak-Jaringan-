import hashlib
import secrets
import base64
import json
from datetime import datetime
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

SECRET_KEY_TEXT = "cuan-tracker-secret-key-2026"


def get_aes_key() -> bytes:
    # Menghasilkan key AES-256 sepanjang 32 byte.
    return hashlib.sha256(SECRET_KEY_TEXT.encode("utf-8")).digest()


# Session sementara di memory. Jika server dimatikan, session hilang.
ACTIVE_SESSIONS = {}


def hash_text(text: str) -> str:
    # Mengubah teks biasa menjadi hash SHA-256.
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def verify_hash(plain_text: str, hashed_text: str) -> bool:
    # Mengecek input user dengan hash yang tersimpan.
    return hash_text(plain_text) == hashed_text


def encrypt_payload(payload: dict) -> str:
    # Mengenkripsi payload JSON menggunakan AES-256-GCM.
    aes_key = get_aes_key()
    aesgcm = AESGCM(aes_key)

    nonce = secrets.token_bytes(12)
    plaintext = json.dumps(payload).encode("utf-8")
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    encrypted_data = nonce + ciphertext
    return base64.b64encode(encrypted_data).decode("utf-8")


def decrypt_payload(encrypted_payload: str) -> dict:
    # Mendekripsi payload AES-256-GCM.
    aes_key = get_aes_key()
    aesgcm = AESGCM(aes_key)

    encrypted_data = base64.b64decode(encrypted_payload.encode("utf-8"))
    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]

    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return json.loads(plaintext.decode("utf-8"))


def generate_session_token() -> str:
    # Membuat session token acak untuk user yang berhasil login.
    return secrets.token_hex(32)


def create_session(user_id: int, username: str, company_key: str) -> str:
    # Membuat session baru dan menyimpan company_key.
    token = generate_session_token()

    ACTIVE_SESSIONS[token] = {
        "user_id": user_id,
        "username": username,
        "company_key": company_key,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return token


def verify_session(token: str):
    # Mengecek apakah session token valid.
    if not token:
        return None

    return ACTIVE_SESSIONS.get(token)


def delete_session(token: str) -> bool:
    # Menghapus session saat user logout.
    if token in ACTIVE_SESSIONS:
        del ACTIVE_SESSIONS[token]
        return True

    return False


def extract_token_from_auth_header(authorization: str):
    # Mengambil token dari header Authorization: Bearer <token>.
    if not authorization:
        return None

    parts = authorization.split()

    if len(parts) != 2:
        return None

    scheme, token = parts

    if scheme.lower() != "bearer":
        return None

    return token
