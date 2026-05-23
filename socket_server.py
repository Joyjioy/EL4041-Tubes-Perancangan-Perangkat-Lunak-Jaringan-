import socket
import json
import threading

from database import init_db
from auth_service import register_user, login_user, logout_user
from transaction_service import add_transaction, get_transactions, get_summary
from security import encrypt_payload, decrypt_payload


HOST = "0.0.0.0"
PORT = 9000
BUFFER_SIZE = 4096


def make_response(status: str, message: str, data=None) -> dict:
    response = {
        "status": status,
        "message": message
    }

    if data is not None:
        response["data"] = data

    return response


def process_decrypted_request(request_data: dict) -> dict:
    # Memproses data setelah didekripsi.
    # Format setelah decrypt:
    # {
    #     "action": "...",
    #     "payload": {...}
    # }

    if "action" not in request_data:
        return make_response("error", "Field action wajib ada")

    if "payload" not in request_data:
        return make_response("error", "Field payload wajib ada")

    action = request_data["action"]
    payload = request_data["payload"]

    try:
        if action == "register":
            return register_user(
                username=payload.get("username"),
                password=payload.get("password"),
                pin=payload.get("pin"),
                device_id=payload.get("device_id")
            )

        elif action == "login":
            return login_user(
                username=payload.get("username"),
                password=payload.get("password"),
                device_id=payload.get("device_id")
            )

        elif action == "add_transaction":
            session_token = payload.get("session_token")

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

            return add_transaction(session_token, transaction_data)

        elif action == "get_transactions":
            return get_transactions(
                session_token=payload.get("session_token"),
                start_date=payload.get("start_date"),
                end_date=payload.get("end_date")
            )

        elif action == "get_summary":
            return get_summary(
                session_token=payload.get("session_token"),
                start_date=payload.get("start_date"),
                end_date=payload.get("end_date")
            )

        elif action == "logout":
            return logout_user(
                session_token=payload.get("session_token")
            )

        else:
            return make_response("error", f"Action tidak dikenal: {action}")

    except Exception as e:
        return make_response("error", f"Terjadi error: {str(e)}")


def process_socket_message(raw_request: dict) -> dict:
    # Menerima request socket dalam bentuk:
    # {
    #     "encrypted_payload": "..."
    # }

    # Lalu decrypt encrypted_payload, proses action, encrypt response

    if "encrypted_payload" not in raw_request:
        response = make_response("error", "Field encrypted_payload wajib ada")
        return {
            "encrypted_payload": encrypt_payload(response)
        }

    try:
        decrypted_request = decrypt_payload(raw_request["encrypted_payload"])
    except Exception:
        response = make_response("error", "Payload gagal didekripsi")
        return {
            "encrypted_payload": encrypt_payload(response)
        }

    response = process_decrypted_request(decrypted_request)

    return {
        "encrypted_payload": encrypt_payload(response)
    }


def handle_client(client_socket, client_address):
    print(f"[CONNECTED] Client terhubung dari {client_address}")

    try:
        data = client_socket.recv(BUFFER_SIZE)

        if not data:
            response = {
                "encrypted_payload": encrypt_payload(
                    make_response("error", "Data kosong")
                )
            }
        else:
            try:
                request_text = data.decode("utf-8")
                raw_request = json.loads(request_text)

                print(f"[REQUEST RAW] {client_address}: {raw_request}")

                response = process_socket_message(raw_request)

                print(f"[RESPONSE ENCRYPTED] {client_address}: {response}")

            except json.JSONDecodeError:
                response = {
                    "encrypted_payload": encrypt_payload(
                        make_response("error", "Format JSON tidak valid")
                    )
                }

        response_text = json.dumps(response)
        client_socket.sendall(response_text.encode("utf-8"))

    except Exception as e:
        error_response = {
            "encrypted_payload": encrypt_payload(
                make_response("error", f"Server error: {str(e)}")
            )
        }
        client_socket.sendall(json.dumps(error_response).encode("utf-8"))

    finally:
        client_socket.close()
        print(f"[DISCONNECTED] Client {client_address} terputus")


def start_socket_server():
    init_db()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"[STARTED] Socket server berjalan di {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()

            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )

            client_thread.start()

    except KeyboardInterrupt:
        print("\n[STOPPED] Socket server dihentikan")

    finally:
        server_socket.close()


if __name__ == "__main__":
    start_socket_server()