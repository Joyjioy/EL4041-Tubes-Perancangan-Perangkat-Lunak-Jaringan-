from typing import Optional
from fastapi import FastAPI, Header
from pydantic import BaseModel

from database import init_db
from auth_service import register_user, login_user, logout_user
from transaction_service import add_transaction, get_transactions, get_summary
from security import extract_token_from_auth_header, decrypt_payload, encrypt_payload


app = FastAPI(title="Cuan Tracker API")


# Inisialisasi database saat server mulai
@app.on_event("startup")
def startup_event():
    init_db()


# Model request terenkripsi
class EncryptedRequest(BaseModel):
    encrypted_payload: str


# Ambil token dari header Authorization
def get_token_from_header(authorization: Optional[str]):
    token = extract_token_from_auth_header(authorization)

    if not token:
        return None

    return token


# Format response sukses terenkripsi
def success_response(message: str, data=None):
    payload = {
        "status": "success",
        "message": message
    }

    if data is not None:
        payload["data"] = data

    return {
        "encrypted_payload": encrypt_payload(payload)
    }


# Format response error terenkripsi
def error_response(message: str):
    payload = {
        "status": "error",
        "message": message
    }

    return {
        "encrypted_payload": encrypt_payload(payload)
    }


# Dekripsi request dari client
def decrypt_request(request: EncryptedRequest):
    try:
        return decrypt_payload(request.encrypted_payload)
    except Exception:
        return None


# Register user baru
@app.post("/register")
def register(request: EncryptedRequest):
    payload = decrypt_request(request)

    if payload is None:
        return error_response("Payload gagal didekripsi")

    result = register_user(
        username=payload.get("username"),
        password=payload.get("password"),
        pin=payload.get("pin"),
        device_id=payload.get("device_id")
    )

    return {
        "encrypted_payload": encrypt_payload(result)
    }


# Login user
@app.post("/login")
def login(request: EncryptedRequest):
    payload = decrypt_request(request)

    if payload is None:
        return error_response("Payload gagal didekripsi")

    result = login_user(
        username=payload.get("username"),
        password=payload.get("password"),
        device_id=payload.get("device_id")
    )

    return {
        "encrypted_payload": encrypt_payload(result)
    }


# Logout user
@app.post("/logout")
def logout(authorization: Optional[str] = Header(None)):
    token = get_token_from_header(authorization)

    if not token:
        return error_response("Authorization token tidak valid")

    result = logout_user(token)

    return {
        "encrypted_payload": encrypt_payload(result)
    }


# Tambah transaksi
@app.post("/transactions")
def create_transaction(
    request: EncryptedRequest,
    authorization: Optional[str] = Header(None)
):
    token = get_token_from_header(authorization)

    if not token:
        return error_response("Authorization token tidak valid")

    payload = decrypt_request(request)

    if payload is None:
        return error_response("Payload gagal didekripsi")

    transaction_data = {
        "transaction_type": payload.get("transaction_type"),
        "category": payload.get("category"),
        "amount": payload.get("amount"),
        "transaction_date": payload.get("transaction_date"),
        "department": payload.get("department"),
        "payment_method": payload.get("payment_method"),
        "reference_number": payload.get("reference_number"),
        "notes": payload.get("notes", "")
    }

    result = add_transaction(token, transaction_data)

    return {
        "encrypted_payload": encrypt_payload(result)
    }


# Ambil riwayat transaksi
@app.get("/transactions")
def read_transactions(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    authorization: Optional[str] = Header(None)
):
    token = get_token_from_header(authorization)

    if not token:
        return error_response("Authorization token tidak valid")

    result = get_transactions(
        session_token=token,
        start_date=start_date,
        end_date=end_date
    )

    return {
        "encrypted_payload": encrypt_payload(result)
    }


# Ambil rekap transaksi
@app.get("/summary")
def read_summary(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    authorization: Optional[str] = Header(None)
):
    token = get_token_from_header(authorization)

    if not token:
        return error_response("Authorization token tidak valid")

    result = get_summary(
        session_token=token,
        start_date=start_date,
        end_date=end_date
    )

    return {
        "encrypted_payload": encrypt_payload(result)
    }


# Cek status API
@app.get("/")
def root():
    result = {
        "status": "success",
        "message": "Cuan Tracker API is running with AES-256 payload encryption"
    }

    return {
        "encrypted_payload": encrypt_payload(result)
    }