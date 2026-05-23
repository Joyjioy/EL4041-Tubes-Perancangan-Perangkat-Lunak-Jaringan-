# EL4041-Tubes-Perancangan-Perangkat-Lunak-Jaringan-

# Cuan Tracker Server

Cuan Tracker Server adalah backend untuk aplikasi pencatatan cashflow perusahaan. Server ini menerima request dari dua jenis client:

1. Client HP/Tablet melalui REST API.
2. Client PC/Laptop melalui TCP Socket.

Kedua jalur komunikasi menggunakan logic dan database yang sama.

---

## 1. Fitur Server

Server mendukung fitur berikut:

- Register user
- Login user
- Logout user
- Device binding menggunakan `device_id`
- Session token
- Tambah transaksi pemasukan/pengeluaran
- Ambil riwayat transaksi
- Ambil rekap cashflow
- Penyimpanan data menggunakan SQLite
- Hash password dan PIN menggunakan SHA-256
- Enkripsi payload menggunakan AES-256

---

## 2. Struktur Folder

```text
cuan_tracker_server/
│
├── database.py
├── security.py
├── auth_service.py
├── transaction_service.py
├── main_api.py
├── socket_server.py
├── run_server.py
├── test_api_encrypted.py
├── test_socket_client.py
└── cuan_tracker.db
```

Keterangan file:

| File | Fungsi |
|---|---|
| `database.py` | Koneksi SQLite dan pembuatan tabel |
| `security.py` | SHA-256, AES-256, session token, authorization helper |
| `auth_service.py` | Register, login, logout, dan session user |
| `transaction_service.py` | Logic transaksi dan summary |
| `main_api.py` | REST API FastAPI pada port 8000 |
| `socket_server.py` | TCP Socket server pada port 9000 |
| `run_server.py` | Menjalankan REST API dan socket server bersamaan |
| `test_api_encrypted.py` | Test client untuk REST API terenkripsi |
| `test_socket_client.py` | Test client untuk socket terenkripsi |

---

## 3. Instalasi Dependency

Pastikan Python sudah terpasang.

Install library yang dibutuhkan:

```bash
pip install fastapi uvicorn cryptography requests
```

---

## 4. Menjalankan Server

Jalankan server dengan perintah:

```bash
python run_server.py
```

Jika berhasil, server akan menjalankan dua layanan:

```text
REST API FastAPI : port 8000
TCP Socket       : port 9000
```

REST API dapat diakses melalui:

```text
http://127.0.0.1:8000
```

Dokumentasi Swagger FastAPI dapat diakses melalui:

```text
http://127.0.0.1:8000/docs
```

Socket server berjalan pada:

```text
127.0.0.1:9000
```

---

## 5. Akses dari Perangkat Lain

Jika client berada di perangkat lain tetapi masih dalam jaringan Wi-Fi yang sama, gunakan IP laptop/server.

Cek IP server di Windows:

```bash
ipconfig
```

Cari bagian IPv4 Address, misalnya:

```text
192.168.1.10
```

Maka alamat server menjadi:

```text
REST API : http://192.168.1.10:8000
Socket   : 192.168.1.10:9000
```

---

## 6. Database

Server menggunakan SQLite dengan nama file:

```text
cuan_tracker.db
```

Tabel utama:

```text
users
transactions
```

### Tabel `users`

Menyimpan data akun user.

| Kolom | Keterangan |
|---|---|
| `user_id` | ID unik user |
| `username` | Username user |
| `password_hash` | Password dalam bentuk hash SHA-256 |
| `pin_hash` | PIN dalam bentuk hash SHA-256 |
| `device_id` | ID perangkat yang terdaftar |
| `created_at` | Waktu pembuatan akun |

### Tabel `transactions`

Menyimpan data transaksi cashflow.

| Kolom | Keterangan |
|---|---|
| `transaction_id` | ID unik transaksi |
| `user_id` | ID user pemilik transaksi |
| `transaction_type` | Pemasukan / Pengeluaran |
| `category` | Kategori transaksi |
| `amount` | Jumlah transaksi |
| `transaction_date` | Tanggal transaksi |
| `department` | Departemen terkait |
| `payment_method` | Metode pembayaran |
| `reference_number` | Nomor invoice/referensi |
| `notes` | Catatan tambahan |
| `created_at` | Waktu transaksi dibuat |

---

## 7. Keamanan

### SHA-256

Password dan PIN tidak disimpan dalam bentuk asli. Server mengubah password dan PIN menjadi hash menggunakan SHA-256 sebelum disimpan ke database.

Alur:

```text
password/PIN asli
↓
hash SHA-256
↓
disimpan ke database
```

### AES-256

Payload request dan response dikirim dalam bentuk terenkripsi menggunakan AES-256.

Format request terenkripsi:

```json
{
  "encrypted_payload": "hasil_enkripsi_AES"
}
```

Server akan melakukan dekripsi payload sebelum memproses data.

Format response terenkripsi:

```json
{
  "encrypted_payload": "hasil_enkripsi_AES"
}
```

Client perlu melakukan dekripsi untuk membaca isi response.

### Session Token

Setelah login berhasil, server mengirimkan `session_token`.

Token ini digunakan untuk mengakses endpoint yang membutuhkan autentikasi, seperti tambah transaksi, ambil transaksi, summary, dan logout.

Untuk REST API, token dikirim melalui header:

```text
Authorization: Bearer <session_token>
```

Untuk socket, token dikirim di dalam payload.

### Device Binding

Saat register, client mengirim `device_id`. Server menyimpan `device_id` tersebut.

Saat login, server membandingkan `device_id` dari client dengan `device_id` yang tersimpan di database.

Jika tidak cocok, login ditolak.

---

## 8. REST API

REST API berjalan pada port 8000.

Base URL lokal:

```text
http://127.0.0.1:8000
```

Endpoint yang tersedia:

| Method | Endpoint | Fungsi |
|---|---|---|
| `POST` | `/register` | Register user baru |
| `POST` | `/login` | Login user |
| `POST` | `/logout` | Logout user |
| `POST` | `/transactions` | Tambah transaksi |
| `GET` | `/transactions` | Ambil riwayat transaksi |
| `GET` | `/summary` | Ambil rekap transaksi |
| `GET` | `/` | Cek status API |

Semua request dan response REST API menggunakan `encrypted_payload`.

### Contoh isi payload sebelum dienkripsi untuk register

```json
{
  "username": "joyfinance",
  "password": "password123",
  "pin": "123456",
  "device_id": "device-mobile-001"
}
```

### Contoh isi payload sebelum dienkripsi untuk login

```json
{
  "username": "joyfinance",
  "password": "password123",
  "device_id": "device-mobile-001"
}
```

### Contoh isi payload sebelum dienkripsi untuk tambah transaksi

```json
{
  "transaction_type": "Pengeluaran",
  "category": "Operasional",
  "amount": 300000,
  "transaction_date": "2026-05-22",
  "department": "Operations",
  "payment_method": "Transfer Bank",
  "reference_number": "TRX-001",
  "notes": "Pembelian perlengkapan kantor"
}
```

---

## 9. TCP Socket

Socket server berjalan pada port 9000.

Alamat lokal:

```text
127.0.0.1:9000
```

Format data yang dikirim client socket:

```json
{
  "encrypted_payload": "hasil_enkripsi_AES"
}
```

Isi sebelum dienkripsi harus memiliki format:

```json
{
  "action": "nama_action",
  "payload": {}
}
```

Daftar action:

| Action | Fungsi |
|---|---|
| `register` | Register user baru |
| `login` | Login user |
| `logout` | Logout user |
| `add_transaction` | Tambah transaksi |
| `get_transactions` | Ambil riwayat transaksi |
| `get_summary` | Ambil rekap transaksi |

### Contoh isi sebelum dienkripsi untuk login socket

```json
{
  "action": "login",
  "payload": {
    "username": "joyfinance",
    "password": "password123",
    "device_id": "device-pc-001"
  }
}
```

### Contoh isi sebelum dienkripsi untuk tambah transaksi socket

```json
{
  "action": "add_transaction",
  "payload": {
    "session_token": "token-dari-login",
    "transaction_type": "Pengeluaran",
    "category": "Operasional",
    "amount": 250000,
    "transaction_date": "2026-05-22",
    "department": "Operations",
    "payment_method": "Cash",
    "reference_number": "SOCK-TRX-001",
    "notes": "Transaksi dari socket client"
  }
}
```

---

## 10. Data Transaksi

Field transaksi yang digunakan:

| Field | Wajib | Keterangan |
|---|---|---|
| `transaction_type` | Ya | Pemasukan / Pengeluaran |
| `category` | Ya | Kategori transaksi |
| `amount` | Ya | Nominal transaksi |
| `transaction_date` | Ya | Tanggal transaksi |
| `department` | Ya | Departemen terkait |
| `payment_method` | Ya | Metode pembayaran |
| `reference_number` | Ya | Nomor invoice/referensi |
| `notes` | Tidak | Catatan tambahan |

### Kategori Pemasukan

```text
Penjualan Produk/Jasa
Investasi
Modal Masuk
Pembayaran Piutang
Pendapatan Bunga
Refund/Reimbursement Masuk
Pendapatan Lainnya
```

### Kategori Pengeluaran

```text
Operasional
Tenaga Kerja/Gaji
Logistik
Administrasi
Pembelian Aset/Inventaris
Marketing & Promosi
Sewa & Utilitas
Transportasi & Perjalanan Dinas
Pajak & Legal
Riset & Pengembangan
Pengeluaran Lainnya
```

### Departemen

```text
Finance & Accounting
Sales & Marketing
Human Resources
Research & Development
Legal & Administration
Operations
```

### Metode Pembayaran

```text
Cash
Transfer Bank
Kartu Perusahaan
Giro
QRIS
E-Wallet
```

---

## 11. Testing

### Test REST API terenkripsi

Pastikan server sudah berjalan:

```bash
python run_server.py
```

Jalankan test REST API:

```bash
python test_api_encrypted.py
```

### Test socket terenkripsi

Pastikan server sudah berjalan:

```bash
python run_server.py
```

Jalankan test socket:

```bash
python test_socket_client.py
```

Jika berhasil, output akan menunjukkan:

```text
Registrasi berhasil
Login berhasil
Transaksi berhasil disimpan
Data transaksi berhasil diambil
Rekap transaksi berhasil dihitung
Logout berhasil
```

Jika muncul pesan `Username sudah digunakan`, itu tidak selalu error. Artinya username tersebut sudah pernah didaftarkan. Login masih bisa dilakukan selama password dan device_id sesuai.

---

## 12. Catatan Pengembangan

Beberapa hal yang bisa dikembangkan:

- Menyimpan session token ke database agar tidak hilang saat server restart.
- Menggunakan password hashing yang lebih kuat seperti bcrypt atau Argon2.
- Menyimpan secret key AES di environment variable.
- Menambahkan fitur reset device.
- Menambahkan fitur export transaksi.
- Menambahkan role user seperti admin dan staff.
- Menambahkan validasi tanggal yang lebih ketat.
- Menambahkan pagination untuk riwayat transaksi.
