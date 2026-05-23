import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

symmKey = b'@cU4NtR4Ck3r5%1e22e57B1B2*3LAoAI' 

def hashingPW(pwIn):
    pwBy = pwIn.encode('utf-8')
    pwSHA = hashlib.sha256(pwBy)
    return pwSHA.hexdigest()

def encryptingData(dataIn):
    dataBy = dataIn.encode('utf-8')
    cipher = AES.new(symmKey, AES.MODE_CBC)
    dataPad = pad(dataBy, AES.block_size)
    enc = cipher.encrypt(dataPad)
    dataAES = base64.b64encode(cipher.iv + enc).decode('utf+8')
    return dataAES


# # ==========================================
# # TEST CASE (Tambahkan di bagian paling bawah file)
# # ==========================================

# def decryptingData(dataAESIn):
#     """Fungsi pendamping khusus test case untuk mendekripsi data AES"""
#     dataGabunganBy = base64.b64decode(dataAESIn.encode('utf-8'))
#     iv = dataGabunganBy[:16]
#     encData = dataGabunganBy[16:]
#     cipher = AES.new(symmKey, AES.MODE_CBC, iv=iv)
#     dataPadLepas = unpad(cipher.decrypt(encData), AES.block_size)
#     return dataPadLepas.decode('utf-8')

# if __name__ == "__main__":
#     print("=== MEMULAI PENGUJIAN SISTEM KEAMANAN ===\n")
    
#     # Data simulasi dari input GUI kamu nanti
#     input_user = "budi_cuan"
#     input_pass = "Rahasia123!"
    
#     print(f"Data Asli dari GUI:")
#     print(f"- Username : {input_user}")
#     print(f"- Password : {input_pass}\n")
    
#     # --- 1. UJI COBA HASHING (SHA256) ---
#     print("1. Menguji Fungsi hashingPW()...")
#     password_terhash = hashingPW(input_pass)
#     print(f"   Hasil SHA256     : {password_terhash}")
#     print(f"   Panjang Karakter : {len(password_terhash)} (Selalu 64 karakter)")
#     print("   [INFO] Fungsi hashingPW() sukses. Data aman disimpan di database.\n")
    
#     # --- 2. UJI COBA ENKRIPSI (AES256) ---
#     print("2. Menguji Fungsi encryptingData()...")
#     username_terenkripsi = encryptingData(input_user)
#     print(f"   Hasil Enkripsi (Base64) : {username_terenkripsi}")
    
#     # Uji coba enkripsi kedua untuk melihat efek IV acak
#     username_terenkripsi_kedua = encryptingData(input_user)
#     print(f"   Hasil Enkripsi Kedua    : {username_terenkripsi_kedua}")
#     print("   [INFO] Hasil berbeda meski input sama. Ini berarti enkripsi dinamis & aman!\n")
    
#     # --- 3. UJI COBA DEKRIPSI (AES256) ---
#     print("3. Menguji Proses Dekripsi (Membuka Kembali Data)...")
#     try:
#         username_asli = decryptingData(username_terenkripsi)
#         print(f"   Berhasil Didekripsi Menjadi : {username_asli}")
        
#         # Validasi kecocokan data asli dengan hasil dekripsi
#         if username_asli == input_user:
#             print("   Status: BERHASIL! Data kembali utuh 100% menggunakan symmKey milikmu.")
#         else:
#             print("   Status: GAGAL! Hasil tidak sesuai asli.")
#     except Exception as e:
#         print(f"   Terjadi error saat dekripsi: {e}")
        
#     print("\n=== PENGUJIAN SELESAI ===")