import hashlib
import secrets
import base64
import json

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


SECRET_KEY_TEXT = "cuan-tracker-secret-key-2026"


def get_aes_key() -> bytes:
    return hashlib.sha256(SECRET_KEY_TEXT.encode("utf-8")).digest()


def encrypt_payload(payload: dict) -> str:
    aes_key = get_aes_key()
    aesgcm = AESGCM(aes_key)

    nonce = secrets.token_bytes(12)
    plaintext = json.dumps(payload).encode("utf-8")
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    return base64.b64encode(nonce + ciphertext).decode("utf-8")


def decrypt_payload(encrypted_payload: str) -> dict:
    aes_key = get_aes_key()
    aesgcm = AESGCM(aes_key)

    encrypted_data = base64.b64decode(encrypted_payload.encode("utf-8"))
    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]

    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return json.loads(plaintext.decode("utf-8"))