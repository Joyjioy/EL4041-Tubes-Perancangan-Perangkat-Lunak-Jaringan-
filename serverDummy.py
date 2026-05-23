import asyncio
import websockets
import json
import hashlib

HOST = "127.0.0.1"
PORT = 9001

# Simulasi Database Sederhana di dalam RAM Server
DATABASE_TRANSAKSI = [
    {
        "transaction_date": "2026-05-20",
        "transaction_type": "Pemasukan",
        "category": "Penjualan Produk/Jasa",
        "amount": 15000000,
        "department": "Sales & Marketing",
        "payment_method": "Transfer Bank",
        "reference_number": "INV/20/05/26/01",
        "notes": "DP Project Aplikasi Web"
    },
    {
        "transaction_date": "2026-05-22",
        "transaction_type": "Pengeluaran",
        "category": "Operasional",
        "amount": 2350000,
        "department": "Finance & Accounting",
        "payment_method": "Cash",
        "reference_number": "INV/22/05/26/02",
        "notes": "Beli ATK dan Token Listrik Kantor"
    }
]

def server_hashing_password(plain_password):
    """Simulasi: Server melakukan hashing SHA256 terhadap password plain dari client"""
    return hashlib.sha256(plain_password.encode('utf-8')).hexdigest()

def hitung_rekap():
    """Fungsi pembantu server untuk mengkalkulasi rekap finansial secara dinamis"""
    total_income = 0
    total_expense = 0
    
    for tx in DATABASE_TRANSAKSI:
        if tx["transaction_type"] == "Pemasukan":
            total_income += tx["amount"]
        elif tx["transaction_type"] == "Pengeluaran":
            total_expense += tx["amount"]
            
    current_balance = total_income - total_expense
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "current_balance": current_balance
    }

async def router_request(websocket, path=None):
    print(f"[WS KONEKSI IN] Client terhubung via WebSocket.")
    try:
        async for message in websocket:
            request_json = json.loads(message)
            action = request_json.get("action")
            payload = request_json.get("payload", {})
            
            print(f"\n[REQUEST RECEIVED] Action: '{action}'")
            print(f"[PAYLOAD DATA] {json.dumps(payload, indent=2)}")
            
            respon = {}
            
            if action == "register":
                username_client = payload.get("username")
                password_plain = payload.get("password")
                pin_plain = payload.get("pin")
                client_device_id = payload.get("device_id") # Menerima device ID dari client
                
                # Simulasi pemrosesan keamanan internal server
                password_terhash = server_hashing_password(password_plain)
                print(f"[SERVER SECURITY] Berhasil memproses pendaftaran untuk {username_client}:")
                print(f"  -> Password Hash DB : {password_terhash}")
                print(f"  -> Device ID Client : {client_device_id}")
                
                respon = {
                    "status": "success",
                    "message": "Registrasi berhasil, Device ID client terdaftar."
                }
                
            elif action == "login":
                username_client = payload.get("username")
                password_plain = payload.get("password")
                client_device_id = payload.get("device_id") # Menerima device ID saat login
                
                print(f"[SERVER SECURITY] Memverifikasi login untuk user: {username_client}")
                print(f"[SERVER SECURITY] Mencocokkan Device ID: {client_device_id}")
                
                respon = {
                    "status": "success",
                    "message": "Login berhasil via enkripsi server",
                    "data": {
                        "user_id": 1,
                        "session_token": "token-wss-server-secure-xyz"
                    }
                }
            
            elif action == "add_transaction":
                # Ambil payload data transaksi baru dan masukkan ke database RAM
                DATABASE_TRANSAKSI.append(payload)
                print(f"[DATABASE] Transaksi baru berhasil disimpan! Total data: {len(DATABASE_TRANSAKSI)}")
                
                respon = {
                    "status": "success",
                    "message": "Transaksi berhasil disimpan di server"
                }
                
            elif action == "get_transactions":
                # Kirim list seluruh transaksi saat ini
                respon = {
                    "status": "success",
                    "message": "Data transaksi berhasil diambil",
                    "data": DATABASE_TRANSAKSI
                }
                
            elif action == "get_summary":
                # Hitung rekap riil berdasarkan data transaksi saat ini
                data_rekap = hitung_rekap()
                respon = {
                    "status": "success",
                    "message": "Data rekap berhasil dihitung",
                    "data": data_rekap
                }
                
            elif action == "logout":
                print(f"[LOGOUT] Token '{payload.get('session_token')}' telah dinonaktifkan.")
                respon = {
                    "status": "success",
                    "message": "Logout berhasil"
                }
                
            else:
                respon = {
                    "status": "error", 
                    "message": f"Action '{action}' tidak dikenali oleh server."
                }
                
            # Kirim kembali respon lewat jalur websocket terbuka ke client
            await websocket.send(json.dumps(respon))
            print(f"[RESPONSE SENT] {respon}")
            print("-" * 50)
            
    except websockets.exceptions.ConnectionClosedOK:
        print("[WS KONEKSI OUT] Client memutuskan koneksi dengan baik.")
    except Exception as e:
        print(f"[SERVER ERROR] Terjadi kendala: {e}")

async def main():
    print(f"=== SERVER DUMMY WS CUAN TRACKER AKTIF ===")
    print(f"[INFO] Mendengarkan koneksi WebSocket di ws://{HOST}:{PORT}\n")
    async with websockets.serve(router_request, HOST, PORT):
        await asyncio.Future()  # Menjaga server tetap berjalan terus-menerus

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[INFO] Server dummy dimatikan.")