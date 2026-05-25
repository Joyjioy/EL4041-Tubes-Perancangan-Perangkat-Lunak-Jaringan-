# import c2_security
import c2_network
import uuid

def deviceIDgen():
    return str(uuid.uuid4())
               
def loggingIn(unameEntry, pwEntry, pinEntry, errorLabel, window):
    print("Mengecek validasi data log in...")
    user = unameEntry.get()
    pwd = pwEntry.get()
    pin = pinEntry.get()
    
    if not user or not pwd or not pin:
        errorLabel.config(text="Semua kolom wajib diisi!", fg="#ab3730")
        return None
    if len(user) < 4 or len(user) > 30:
        errorLabel.config(text="Username harus 4-30 karakter!", fg="#ab3730")
        return None
    if len(pwd) < 8 or len(pwd) > 64:
        errorLabel.config(text="Password harus 8-64 karakter!", fg="#ab3730")
        return None
    if len(pin) < 4 or len(pin) > 8 or not pin.isdigit():
        errorLabel.config(text="PIN harus 4-8 digit angka!", fg="#ab3730")
        return None
        
    errorLabel.config(text="Memvalidasi data...", fg="#3f49a5")
    window.update()

    try:
        with open("deviceID.txt", "r") as file:
            deviceIDc = file.read().strip()
    except FileNotFoundError:
        deviceIDc = ""

    payload = {
        "username": user,  # Teks biasa
        "password": pwd,    # Teks biasa
        "device_id": deviceIDc
    }
    
    respon = c2_network.sendSocket("login", payload)
    
    if respon.get("status") == "success":
        errorLabel.config(text="Login Berhasil!", fg="#3f49a5")
        return respon["data"]["session_token"]
    else:
        errorMessage = respon.get("message", "Gagal log in.")
        errorLabel.config(text=errorMessage, fg="#ab3730")
        return None


def signingUp(unameSEntry, pwSEntry, pinSEntry, errorSLabel, window):
    print("Mengecek validasi data sign up...")
    user = unameSEntry.get()
    pwd = pwSEntry.get()
    pin = pinSEntry.get()
    
    # Validasi Constraints
    if not user or not pwd or not pin:
        errorSLabel.config(text="Semua kolom wajib diisi!", fg="#ab3730")
        return False
    if len(user) < 4 or len(user) > 30:
        errorSLabel.config(text="Username harus 4-30 karakter!", fg="#ab3730")
        return False
    if len(pwd) < 8 or len(pwd) > 64:
        errorSLabel.config(text="Password harus 8-64 karakter!", fg="#ab3730")
        return False
    if len(pin) < 4 or len(pin) > 8 or not pin.isdigit():
        errorSLabel.config(text="PIN harus 4-8 digit angka!", fg="#ab3730")
        return False
        
    errorSLabel.config(text="Mendaftarkan akun...", fg="#3f49a5")
    window.update()
    
    deviceID = deviceIDgen()

    payload = {
        "username": user,
        "password": pwd,
        "pin": pin,
        "device_id": deviceID
    }
        
    respon = c2_network.sendSocket("register", payload)
    
    if respon.get("status") == "success":
        with open("deviceID.txt", "w") as file:
            file.write(deviceID)
            
        errorSLabel.config(text="Registrasi berhasil dilakukan.", fg="#3f49a5")
        return True
    else:
        errorMessage = respon.get("message", "Registrasi gagal dilakukan.")
        errorSLabel.config(text=errorMessage, fg="#ab3730")
        return False
    

def addTrans(typeVar, categoryVar, amountVar, tanggalString, deptVar, payVar, invoiceEntry, notesEntry, errorHomeLabel, window, tokenSesi):
    print("Menunggu input data...")
    
    tipe = typeVar.get().strip()
    kategori = categoryVar.get().strip()
    jumlah = amountVar.get().strip()  # Sekarang membaca dari StringVar dengan aman
    departemen = deptVar.get().strip()
    metode = payVar.get().strip()
    invoice = invoiceEntry.get().strip()
    notes = notesEntry.get().strip()
    tanggal = tanggalString 
    
    # 1. Validasi Kolom Wajib
    if not tipe or not kategori or not jumlah or not departemen or not metode or not invoice:
        errorHomeLabel.config(text="Semua kolom wajib (kecuali Notes) harus diisi!", fg="#ab3730")
        return False
        
    # 2. Validasi Batasan Karakter Notes
    if len(notes) > 100:
        errorHomeLabel.config(text="Notes maksimal 100 karakter!", fg="#ab3730")
        return False

    # 3. Validasi Format Dasar Invoice (INV/DD/MM/YY/XX -> Panjang minimal 16 karakter)
    if not invoice.startswith("INV/") or len(invoice) < 15:
        errorHomeLabel.config(text="Format Invoice salah! (Harus INV/DD/MM/YY/XX)", fg="#ab3730")
        return False

    errorHomeLabel.config(text="Menyimpan data transaksi...", fg="#3f49a5")
    window.update()

    # Bersihkan titik ribuan sebelum dikonversi ke integer murni
    jumlah_bersih = jumlah.replace('.', '')

    payload = {
        "session_token": tokenSesi,
        "transaction_type": tipe,
        "category": kategori,
        "amount": int(jumlah_bersih),
        "transaction_date": tanggal,
        "department": departemen,
        "payment_method": metode,
        "reference_number": invoice,
        "notes": notes 
    }
    
    respon = c2_network.sendSocket("add_transaction", payload)
    
    if respon.get("status") == "success":
        errorHomeLabel.config(text="Data transaksi berhasil ditambahkan.", fg="#3f49a5")
        return True
    else:
        errorMessage = respon.get("message", "Gagal menambahkan transaksi.")
        errorHomeLabel.config(text=errorMessage, fg="#ab3730")
        return False
    
def getTrans(tokenSesi, errorLabel, window):
    print("Mengambil data transaksi dari server...")
    
    if not tokenSesi:
        errorLabel.config(text="Sesi habis, silakan login kembali!", fg="#ab3730")
        return None
        
    payload = {
        "session_token": tokenSesi
    }
    
    # Kirim request ke server (sesuaikan nama action "get_transactions" dengan spek servermu)
    respon = c2_network.sendSocket("get_transactions", payload)
    
    if respon.get("status") == "success":
        # Mengembalikan list data transaksi yang dikirim oleh server
        return respon.get("data", [])  
    else:
        errorMessage = respon.get("message", "Gagal mengambil data transaksi.")
        errorLabel.config(text=errorMessage, fg="#ab3730")
        return None
    
def getSummary(tokenSesi, errorLabel, window):
    print("Mengambil data rekap finansial dari server...")
    
    if not tokenSesi:
        errorLabel.config(text="Sesi habis, silakan login kembali!", fg="#ab3730")
        return None
        
    payload = {
        "session_token": tokenSesi
    }
    
    # Kirim request rekap ke server via socket
    respon = c2_network.sendSocket("get_summary", payload)
    
    if respon.get("status") == "success":
        # Mengembalikan data finansial (misal berupa dictionary berisi total pemasukan, pengeluaran, saldo)
        return respon.get("data", {})
    else:
        errorMessage = respon.get("message", "Gagal mengambil data rekap.")
        errorLabel.config(text=errorMessage, fg="#ab3730")
        return None
    
def logout(tokenSesi):
    print("Mengirim perintah log out ke server...")
    if not tokenSesi:
        return True
    
    payload = {
        "session_token": tokenSesi
    }
    # Kirim action logout ke server
    respon = c2_network.sendSocket("logout", payload)
    return respon.get("status") == "success"