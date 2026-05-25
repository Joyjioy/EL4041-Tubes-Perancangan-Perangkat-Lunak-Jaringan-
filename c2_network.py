import socket
import json

from c2_security import encrypt_payload, decrypt_payload


SERVER_HOST = "10.5.101.50"  # Ganti sesuai IP laptop server
SERVER_PORT = 9000
BUFFER_SIZE = 4096


def sendSocket(actionName, payloadData):
    request_data = {
        "action": actionName,
        "payload": payloadData
    }

    encrypted_request = {
        "encrypted_payload": encrypt_payload(request_data)
    }

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        request_text = json.dumps(encrypted_request)
        client_socket.sendall(request_text.encode("utf-8"))

        response = client_socket.recv(BUFFER_SIZE)
        client_socket.close()

        response_json = json.loads(response.decode("utf-8"))
        decrypted_response = decrypt_payload(response_json["encrypted_payload"])

        return decrypted_response

    except Exception as e:
        return {
            "status": "error",
            "message": f"Gagal terhubung ke socket server: {str(e)}"
        }