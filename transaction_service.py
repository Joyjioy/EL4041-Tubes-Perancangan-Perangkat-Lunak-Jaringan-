from database import get_connection, get_current_timestamp
from auth_service import get_user_from_session


VALID_TRANSACTION_TYPES = [
    "Pemasukan",
    "Pengeluaran"
]

VALID_INCOME_CATEGORIES = [
    "Penjualan Produk/Jasa",
    "Investasi",
    "Modal Masuk",
    "Pembayaran Piutang",
    "Pendapatan Bunga",
    "Refund/Reimbursement Masuk",
    "Pendapatan Lainnya"
]

VALID_EXPENSE_CATEGORIES = [
    "Operasional",
    "Tenaga Kerja/Gaji",
    "Logistik",
    "Administrasi",
    "Pembelian Aset/Inventaris",
    "Marketing & Promosi",
    "Sewa & Utilitas",
    "Transportasi & Perjalanan Dinas",
    "Pajak & Legal",
    "Riset & Pengembangan",
    "Pengeluaran Lainnya"
]

VALID_DEPARTMENTS = [
    "Finance & Accounting",
    "Sales & Marketing",
    "Human Resources",
    "Research & Development",
    "Legal & Administration",
    "Operations"
]

VALID_PAYMENT_METHODS = [
    "Cash",
    "Transfer Bank",
    "Kartu Perusahaan",
    "Giro",
    "QRIS",
    "E-Wallet"
]


def validate_transaction_data(data: dict) -> dict:
    # Validasi field wajib
    required_fields = [
        "transaction_type",
        "category",
        "amount",
        "transaction_date",
        "department",
        "payment_method",
        "reference_number"
    ]

    for field in required_fields:
        if field not in data or data[field] in [None, ""]:
            return {
                "valid": False,
                "message": f"Field {field} wajib diisi"
            }

    transaction_type = data["transaction_type"]
    category = data["category"]
    amount = data["amount"]
    department = data["department"]
    payment_method = data["payment_method"]
    reference_number = data["reference_number"]
    notes = data.get("notes", "")

    # Validasi tipe dan kategori
    if transaction_type not in VALID_TRANSACTION_TYPES:
        return {
            "valid": False,
            "message": "Tipe transaksi tidak valid"
        }

    if transaction_type == "Pemasukan" and category not in VALID_INCOME_CATEGORIES:
        return {
            "valid": False,
            "message": "Kategori pemasukan tidak valid"
        }

    if transaction_type == "Pengeluaran" and category not in VALID_EXPENSE_CATEGORIES:
        return {
            "valid": False,
            "message": "Kategori pengeluaran tidak valid"
        }

    # Validasi departemen dan metode pembayaran
    if department not in VALID_DEPARTMENTS:
        return {
            "valid": False,
            "message": "Departemen tidak valid"
        }

    if payment_method not in VALID_PAYMENT_METHODS:
        return {
            "valid": False,
            "message": "Metode pembayaran tidak valid"
        }

    # Validasi nominal
    try:
        amount = int(amount)
        if amount <= 0:
            return {
                "valid": False,
                "message": "Nominal transaksi harus lebih dari 0"
            }
    except ValueError:
        return {
            "valid": False,
            "message": "Nominal transaksi harus berupa angka"
        }

    # Validasi panjang teks
    if len(reference_number) > 50:
        return {
            "valid": False,
            "message": "Reference number maksimal 50 karakter"
        }

    if notes and len(notes) > 255:
        return {
            "valid": False,
            "message": "Notes maksimal 255 karakter"
        }

    return {
        "valid": True,
        "message": "Data valid"
    }


def add_transaction(session_token: str, data: dict) -> dict:
    # Cek session user
    session = get_user_from_session(session_token)

    if not session:
        return {
            "status": "error",
            "message": "Session tidak valid. Silakan login ulang."
        }

    validation = validate_transaction_data(data)

    if not validation["valid"]:
        return {
            "status": "error",
            "message": validation["message"]
        }

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO transactions (
                user_id,
                transaction_type,
                category,
                amount,
                transaction_date,
                department,
                payment_method,
                reference_number,
                notes,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                data["transaction_type"],
                data["category"],
                int(data["amount"]),
                data["transaction_date"],
                data["department"],
                data["payment_method"],
                data["reference_number"],
                data.get("notes", ""),
                get_current_timestamp()
            )
        )

        conn.commit()

        return {
            "status": "success",
            "message": "Transaksi berhasil disimpan",
            "data": {
                "transaction_id": cursor.lastrowid
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Gagal menyimpan transaksi: {str(e)}"
        }

    finally:
        conn.close()


def get_transactions(
    session_token: str,
    start_date: str = None,
    end_date: str = None
) -> dict:
    # Cek session user
    session = get_user_from_session(session_token)

    if not session:
        return {
            "status": "error",
            "message": "Session tidak valid. Silakan login ulang."
        }

    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
            SELECT
                transaction_id,
                transaction_type,
                category,
                amount,
                transaction_date,
                department,
                payment_method,
                reference_number,
                notes,
                created_at
            FROM transactions
            WHERE user_id = ?
        """

        params = [session["user_id"]]

        if start_date:
            query += " AND transaction_date >= ?"
            params.append(start_date)

        if end_date:
            query += " AND transaction_date <= ?"
            params.append(end_date)

        query += " ORDER BY transaction_date DESC, transaction_id DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()

        transactions = [
            {
                "transaction_id": row["transaction_id"],
                "transaction_type": row["transaction_type"],
                "category": row["category"],
                "amount": row["amount"],
                "transaction_date": row["transaction_date"],
                "department": row["department"],
                "payment_method": row["payment_method"],
                "reference_number": row["reference_number"],
                "notes": row["notes"],
                "created_at": row["created_at"]
            }
            for row in rows
        ]

        return {
            "status": "success",
            "message": "Data transaksi berhasil diambil",
            "data": {
                "transactions": transactions
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Gagal mengambil transaksi: {str(e)}"
        }

    finally:
        conn.close()


def get_summary(
    session_token: str,
    start_date: str = None,
    end_date: str = None
) -> dict:
    # Cek session user
    session = get_user_from_session(session_token)

    if not session:
        return {
            "status": "error",
            "message": "Session tidak valid. Silakan login ulang."
        }

    conn = get_connection()
    cursor = conn.cursor()

    try:
        base_query = """
            FROM transactions
            WHERE user_id = ?
        """

        params = [session["user_id"]]

        if start_date:
            base_query += " AND transaction_date >= ?"
            params.append(start_date)

        if end_date:
            base_query += " AND transaction_date <= ?"
            params.append(end_date)

        # Total pemasukan
        cursor.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total
            """ + base_query + """
            AND transaction_type = 'Pemasukan'
            """,
            params
        )
        total_income = cursor.fetchone()["total"]

        # Total pengeluaran
        cursor.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total
            """ + base_query + """
            AND transaction_type = 'Pengeluaran'
            """,
            params
        )
        total_expense = cursor.fetchone()["total"]

        # Pemasukan per kategori
        cursor.execute(
            """
            SELECT category, COALESCE(SUM(amount), 0) AS total
            """ + base_query + """
            AND transaction_type = 'Pemasukan'
            GROUP BY category
            """,
            params
        )
        income_by_category = {
            row["category"]: row["total"]
            for row in cursor.fetchall()
        }

        # Pengeluaran per kategori
        cursor.execute(
            """
            SELECT category, COALESCE(SUM(amount), 0) AS total
            """ + base_query + """
            AND transaction_type = 'Pengeluaran'
            GROUP BY category
            """,
            params
        )
        expense_by_category = {
            row["category"]: row["total"]
            for row in cursor.fetchall()
        }

        return {
            "status": "success",
            "message": "Rekap transaksi berhasil dihitung",
            "data": {
                "total_income": total_income,
                "total_expense": total_expense,
                "balance": total_income - total_expense,
                "income_by_category": income_by_category,
                "expense_by_category": expense_by_category
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Gagal menghitung summary: {str(e)}"
        }

    finally:
        conn.close()