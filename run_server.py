import threading
import uvicorn

from database import init_db
from socket_server import start_socket_server


def run_api_server():
    # Menjalankan FastAPI server
    uvicorn.run(
        "main_api:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )


def run_socket_server():
    # Menjalankan socket server
    start_socket_server()


if __name__ == "__main__":
    print("=== CUAN TRACKER SERVER STARTING ===")

    init_db()

    # Jalankan socket server di thread terpisah
    socket_thread = threading.Thread(
        target=run_socket_server,
        daemon=True
    )
    socket_thread.start()

    print("Socket server berjalan")
    
    # Jalankan FastAPI server di main thread
    run_api_server()
    print("FastAPI server berjalan")