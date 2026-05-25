from database import get_connection, get_current_timestamp
from security import hash_text, verify_hash, create_session, verify_session, delete_session


def register_user(username: str, password: str, pin: str, device_id: str) -> dict:
    # Validasi input register
    if not username or not password or not pin or not device_id:
        return {
            "status": "error",
            "message": "Username, password, PIN, dan device_id wajib diisi"
        }

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Cek apakah username sudah terdaftar
        cursor.execute(
            "SELECT user_id FROM users WHERE username = ?",
            (username,)
        )
        existing_user = cursor.fetchone()

        if existing_user:
            return {
                "status": "error",
                "message": "Username sudah digunakan"
            }

        # Password dan PIN disimpan dalam bentuk hash
        password_hash = hash_text(password)
        pin_hash = hash_text(pin)

        # Simpan data user baru ke database
        cursor.execute(
            """
            INSERT INTO users (
                username,
                password_hash,
                pin_hash,
                device_id,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                username,
                password_hash,
                pin_hash,
                device_id,
                get_current_timestamp()
            )
        )

        conn.commit()

        return {
            "status": "success",
            "message": "Registrasi berhasil"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Registrasi gagal: {str(e)}"
        }

    finally:
        conn.close()


def login_user(username: str, password: str, device_id: str) -> dict:
    # Validasi input login
    if not username or not password or not device_id:
        return {
            "status": "error",
            "message": "Username, password, dan device_id wajib diisi"
        }

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Ambil data user berdasarkan username
        cursor.execute(
            """
            SELECT user_id, username, password_hash, device_id
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        user = cursor.fetchone()

        if not user:
            return {
                "status": "error",
                "message": "Username atau password salah"
            }

        # Verifikasi password dengan hash yang tersimpan
        if not verify_hash(password, user["password_hash"]):
            return {
                "status": "error",
                "message": "Username atau password salah"
            }

        # Cek device binding
        if device_id != user["device_id"]:
            return {
                "status": "error",
                "message": "Perangkat tidak terdaftar"
            }

        # Buat session token jika login valid
        session_token = create_session(
            user_id=user["user_id"],
            username=user["username"]
        )

        return {
            "status": "success",
            "message": "Login berhasil",
            "data": {
                "user_id": user["user_id"],
                "session_token": session_token
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Login gagal: {str(e)}"
        }

    finally:
        conn.close()


def logout_user(session_token: str) -> dict:
    # Hapus session token saat user logout
    if not session_token:
        return {
            "status": "error",
            "message": "Session token wajib diisi"
        }

    success = delete_session(session_token)

    if success:
        return {
            "status": "success",
            "message": "Logout berhasil"
        }

    return {
        "status": "error",
        "message": "Session tidak ditemukan"
    }


def get_user_from_session(session_token: str):
    # Mengambil data user dari session aktif
    return verify_session(session_token)