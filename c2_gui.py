from tkinter import *
from tkinter import ttk
import c2_logic 
import os

sesToken = None

def logIn():
    print("Membuka page log in... ")
    errorLabel.config(text="")  
    frameInit.pack_forget()
    frameLogin.pack(fill="both", expand=True)

def signUp():
    print("Membuka page sign up...")
    errorSLabel.config(text="")  
    frameInit.pack_forget()
    frameSignup.pack(fill="both", expand=True)

def handleLogin():
    global sesToken
    token = c2_logic.loggingIn(unameEntry, pwEntry, pinEntry, errorLabel, window)
    if token:
        sesToken = token
        with open("sessionToken.txt", "w") as file:
            file.write(token)
            
        frameLogin.pack_forget()
        goToHome()

def handleSignup():
    sukses = c2_logic.signingUp(unameSEntry, pwSEntry, pinSEntry, errorSLabel, window)
    if sukses:
        errorSLabel.config(text="Registrasi sukses! Silakan Log In.", fg="#3f49a5")
        frameSignup.pack_forget()
        frameLogin.pack(fill="both", expand=True) # Pindah ke form login

def backtoInit():
    frameLogin.pack_forget()
    frameInit.pack(fill="both", expand=True)

def backtoInitS():
    frameSignup.pack_forget()
    frameInit.pack(fill="both", expand=True)

def goToHome():
    print("Membuka page home... ")
    frameHome.pack(fill="both", expand=True)

def handleLogout():
    global sesToken
    print("Melakukan proses log out...")
    
    c2_logic.logout(sesToken)
    sesToken = None
    
    if os.path.exists("sessionToken.txt"):
        os.remove("sessionToken.txt")
        
    frameHome.pack_forget()
    frameInit.pack(fill="both", expand=True)

def menuAdd():
    print("Membuka menu Penambahan Transaksi...")
    frameHome.pack_forget()
    frameAddtrans.pack(fill="both", expand=True)

def backfromAdd():
    errorAdd.config(text="")
    frameAddtrans.pack_forget()
    frameHome.pack(fill="both", expand=True)

def updateKategoriOptions(*args):
    transType = tipeVar.get()
    
    catIncome = [
        "Penjualan Produk/Jasa", "Investasi", "Modal Masuk", 
        "Pembayaran Piutang", "Pendapatan Bunga", "Refund/Reimbursement Masuk", "Pendapatan Lainnya"
    ]
    catExpense = [
        "Operasional", "Tenaga Kerja/Gaji", "Logistik", "Administrasi", 
        "Pembelian Aset/Inventaris", "Marketing & Promosi", "Sewa & Utilitas", 
        "Transportasi & Perjalanan Dinas", "Pajak & Legal", "Riset & Pengembangan", "Pengeluaran Lainnya"
    ]
    
    catMenu['menu'].delete(0, 'end')
    
    newOpt = catIncome if transType == "Pemasukan" else catExpense
    for opsi in newOpt:
        catMenu['menu'].add_command(label=opsi, command=lambda value=opsi: kategoriVar.set(value))
    
    kategoriVar.set(newOpt[0])

def formatRibuan(*args):
    teks_asli = jumlahVar.get().replace('.', '') 
    if teks_asli.isdigit():
        if teks_asli == "0":
            jumlahVar.set("")
        else:
            teks_format = f"{int(teks_asli):,}".replace(',', '.')
            jumlahVar.set(teks_format)
    elif teks_asli == "":
        jumlahVar.set("")
    else:
        jumlahVar.set(jumlahVar.get()[:-1])

def handleaddTrans():
    global sesToken
    
    transDate = f"{tglVar.get()}/{blnVar.get()}/{thnVar.get()}"
    
    sukses = c2_logic.addTrans(
        tipeVar, kategoriVar, jumlahVar, transDate, deptVar, 
        payVar, invoiceEntry, notesEntry, errorAdd, window, sesToken
    )
    
    if sukses:
        errorAdd.config(text="Transaksi berhasil disimpan!", fg="#3f49a5")
        window.update()
        window.after(1500, backfromAdd)

def menuView():
    print("Membuka menu Lihat Transaksi...")
    global sesToken
    
    dataTrans = c2_logic.getTrans(sesToken, errorAdd, window)
    
    if dataTrans is not None:
        frameHome.pack_forget()
        frameViewtrans.pack(fill="both", expand=True)
        
        for row in tableTrans.get_children():
            tableTrans.delete(row)
            
        for tx in dataTrans:
            jumlah_format = f"{int(tx['amount']):,}".replace(',', '.')
            
            tableTrans.insert("", "end", values=(
                tx.get('transaction_date'),
                tx.get('transaction_type'),
                tx.get('category'),
                f"Rp {jumlah_format}",
                tx.get('department'),
                tx.get('payment_method'),
                tx.get('reference_number'),
                tx.get('notes', '')
            ))

def backfromView():
    frameViewtrans.pack_forget()
    frameHome.pack(fill="both", expand=True)

def menuRecap():
    print("Membuka menu Rekap Transaksi...")
    global sesToken
    
    dataSummary = c2_logic.getSummary(sesToken, errorAdd, window)
    
    if dataSummary is not None:
        frameHome.pack_forget()
        frameRecap.pack(fill="both", expand=True)
        
        pemasukan = int(dataSummary.get("total_income", 0))
        pengeluaran = int(dataSummary.get("total_expense", 0))
        saldo = int(dataSummary.get("current_balance", 0))
        
        pemasukanFormat = f"{pemasukan:,}".replace(',', '.')
        pengeluaranFormat = f"{pengeluaran:,}".replace(',', '.')
        saldoFormat = f"{saldo:,}".replace(',', '.')
        
        valIncome.config(text=f"Rp {pemasukanFormat}", fg="#3F49A5")
        valExpense.config(text=f"Rp {pengeluaranFormat}", fg="#ab3730")
        
        if saldo >= 0:
            valSaldo.config(text=f"Rp {saldoFormat}", fg="#3F49A5")
        else:
            valSaldo.config(text=f"Rp {saldoFormat}", fg="#ab3730")

def backfromRec():
    frameRecap.pack_forget()
    frameHome.pack(fill="both", expand=True)


window = Tk()
window.geometry("800x450")  
window.title("Cuan Tracker")

logoOri = PhotoImage(file='logo_ct.png')
logo = logoOri.subsample(8, 8) 

window.iconphoto(True, logo)
window.iconphoto(True, logo)
window.config(background="#FFF8EF")

# ==========================================
# FRAME INITIAL 
# ==========================================
frameInit = Frame(window, bg='#fff8ef')
frameInit.pack(fill="both", expand=True)

titleInit = Label(frameInit, text="Cuan Tracker", font=('Tw Cen MT', 40, 'bold'), fg='#3F49A5', bg='#FFF8EF', image=logo, compound='bottom')
titleInit.pack(pady=10)

loginBt = Button(frameInit, text="Log In", command=logIn, font=('Tw Cen MT', 15, 'bold'), bg='#b6c8df', fg='#3f49a5', activebackground='#3f49a5', activeforeground='#b6c8df')
loginBt.pack()

signupBt = Button(frameInit, text="Sign Up", command=signUp, font=('Tw Cen MT', 15, 'bold'), bg='#b6c8df', fg='#3f49a5', activebackground='#3f49a5', activeforeground='#b6c8df')
signupBt.pack(pady=10)


# ==========================================
# FRAME LOG IN
# ==========================================
frameLogin = Frame(window, bg='#FFF8EF')
titleLogin = Label(frameLogin, text="Log In", font=('Tw Cen MT', 25, 'bold'), fg='#3F49A5', bg='#FFF8EF')
titleLogin.pack(pady=10)

errorLabel = Label(frameLogin, text="", font=('Tw Cen MT', 9, 'bold'), bg='#FFF8EF')
errorLabel.pack(pady=5)

unameLabel = Label(frameLogin, text="Username :", font=('Tw Cen MT', 15), fg='#3F49A5', bg='#FFF8EF')
unameLabel.pack(pady=(5, 0))
unameEntry = Entry(frameLogin, font=('Tw Cen MT', 15), width=30)
unameEntry.pack(pady=5)

pwLabel = Label(frameLogin, text="Password :", font=('Tw Cen MT', 15), fg='#3F49A5', bg='#FFF8EF')
pwLabel.pack(pady=(5, 0))
pwEntry = Entry(frameLogin, font=('Tw Cen MT', 15), width=30, show="•")  # Lebar disamakan dengan username agar rapi
pwEntry.pack(pady=5)

pinLabel = Label(frameLogin, text="PIN Perusahaan :", font=('Tw Cen MT', 15), fg='#3F49A5', bg='#FFF8EF')
pinLabel.pack(pady=(5, 0))
pinEntry = Entry(frameLogin, font=('Tw Cen MT', 15), width=8, show="•")
pinEntry.pack(pady=5)

frameBt = Frame(frameLogin, bg='#FFF8EF')
frameBt.pack(pady=10)

submitBt = Button(frameBt, text="Masuk", font=('Tw Cen MT', 12, 'bold'), bg='#b6c8df', fg='#3f49a5', command=handleLogin)
submitBt.pack(side=LEFT, padx=20)

backBt = Button(frameBt, text="Kembali", font=('Tw Cen MT', 12), bg='#b6c8df', fg='#3f49a5', command=backtoInit)
backBt.pack(side=LEFT, padx=20)


# ==========================================
# FRAME SIGN UP
# ==========================================
frameSignup = Frame(window, bg='#FFF8EF')
titleSignup = Label(frameSignup, text="Sign Up", font=('Tw Cen MT', 25, 'bold'), fg='#3F49A5', bg='#FFF8EF')
titleSignup.pack(pady=10)

errorSLabel = Label(frameSignup, text="", font=('Tw Cen MT', 9, 'bold'), bg='#FFF8EF')
errorSLabel.pack(pady=5)

unameSLabel = Label(frameSignup, text="Username :", font=('Tw Cen MT', 15), fg='#3F49A5', bg='#FFF8EF')
unameSLabel.pack(pady=(5, 0))
unameSEntry = Entry(frameSignup, font=('Tw Cen MT', 15), width=30)
unameSEntry.pack(pady=5)

pwSLabel = Label(frameSignup, text="Password :", font=('Tw Cen MT', 15), fg='#3F49A5', bg='#FFF8EF')
pwSLabel.pack(pady=(5, 0))
pwSEntry = Entry(frameSignup, font=('Tw Cen MT', 15), width=30, show="•") 
pwSEntry.pack(pady=5)

pinSLabel = Label(frameSignup, text="PIN Perusahaan :", font=('Tw Cen MT', 15), fg='#3F49A5', bg='#FFF8EF')
pinSLabel.pack(pady=(5, 0))
pinSEntry = Entry(frameSignup, font=('Tw Cen MT', 15), width=8, show="•")
pinSEntry.pack(pady=5)

frameSBt = Frame(frameSignup, bg='#FFF8EF')
frameSBt.pack(pady=10)

submitSBt = Button(frameSBt, text="Daftar", font=('Tw Cen MT', 12, 'bold'), bg='#b6c8df', fg='#3f49a5', command=handleSignup) 
submitSBt.pack(side=LEFT, padx=20)

backSBt = Button(frameSBt, text="Kembali", font=('Tw Cen MT', 12), bg='#b6c8df', fg='#3f49a5', command=backtoInitS)
backSBt.pack(side=LEFT, padx=20)


# ==========================================
# FRAME HOME
# ==========================================
frameHome = Frame(window, bg='#FFF8EF')

titleHome = Label(frameHome,
                  text="Cuan Tracker",
                  font=('Tw Cen MT', 40, 'bold'), fg='#3F49A5', bg='#FFF8EF',
                  image=logo,
                  compound='bottom'
                  )
titleHome.pack(pady=20)

frameMenu = Frame(frameHome, bg='#FFF8EF')
frameMenu.pack(pady=20)

btAddtrans = Button(frameMenu, text="Tambah Transaksi", command=menuAdd, font=('Tw Cen MT', 12, 'bold'), bg='#b6c8df', fg='#3f49a5')
btAddtrans.pack(side=LEFT, padx=10)

btGettrans = Button(frameMenu, text="Lihat Transaksi", command=menuView, font=('Tw Cen MT', 12, 'bold'), bg='#b6c8df', fg='#3f49a5')
btGettrans.pack(side=LEFT, padx=10)

btGetrecap = Button(frameMenu, text="Rekap Transaksi", command=menuRecap, font=('Tw Cen MT', 12, 'bold'), bg='#b6c8df', fg='#3f49a5')
btGetrecap.pack(side=LEFT, padx=10)

btLogout = Button(frameMenu, text="Log Out", command=handleLogout, font=('Tw Cen MT', 12, 'bold'), bg='#ab3730', fg='white', activebackground='#3f49a5')
btLogout.pack(side=LEFT, padx=10)

# ==========================================
# FRAME TAMBAH DATA TRANSAKSI 
# ==========================================
frameAddtrans = Frame(window, bg='#FFF8EF')

titleTambah = Label(frameAddtrans, text="Penambahan Transaksi", font=('Tw Cen MT', 20, 'bold'), fg='#3F49A5', bg='#FFF8EF')
titleTambah.pack(pady=(1, 5))

errorAdd = Label(frameAddtrans, text="", font=('Tw Cen MT', 8, 'bold'), bg='#FFF8EF')
errorAdd.pack()

formContainer = Frame(frameAddtrans, bg='#FFF8EF')
formContainer.pack(pady=5)

Label(formContainer, text="Tipe Transaksi :", font=('Tw Cen MT', 12), fg='#3F49A5', bg='#FFF8EF').grid(row=0, column=0, sticky=W, pady=5, padx=10)
tipeVar = StringVar(window)
tipeVar.set("Pengeluaran") 
tipeMenu = OptionMenu(formContainer, tipeVar, "Pemasukan", "Pengeluaran") 
tipeMenu.config(width=27, font=('Tw Cen MT', 10), bg='#b6c8df', fg='#3f49a5')
tipeMenu['menu'].config(font=('Tw Cen MT', 10), fg='#3f49a5', bg='#FFF8EF')
tipeMenu.grid(row=0, column=1, sticky=W, pady=5)
tipeVar.trace_add("write", updateKategoriOptions) 

Label(formContainer, text="Kategori :", font=('Tw Cen MT', 12), fg='#3F49A5', bg='#FFF8EF').grid(row=1, column=0, sticky=W, pady=5, padx=10)
kategoriVar = StringVar(window)
catMenu = OptionMenu(formContainer, kategoriVar, "")
catMenu.config(width=27, font=('Tw Cen MT', 10), bg='#b6c8df', fg='#3f49a5')
catMenu['menu'].config(font=('Tw Cen MT', 10), fg='#3f49a5', bg='#FFF8EF')
catMenu.grid(row=1, column=1, sticky=W, pady=5)

Label(formContainer, text="Jumlah (Rp) :", font=('Tw Cen MT', 12), fg='#3F49A5', bg='#FFF8EF').grid(row=2, column=0, sticky=W, pady=5, padx=10)
jumlahVar = StringVar(window)
jumlahVar.trace_add("write", formatRibuan) 
jumlahEntry = Entry(formContainer, textvariable=jumlahVar, font=('Tw Cen MT', 12), width=30)
jumlahEntry.grid(row=2, column=1, sticky=W, pady=5)

Label(formContainer, text="Tanggal Transaksi :", font=('Tw Cen MT', 12), fg='#3F49A5', bg='#FFF8EF').grid(row=3, column=0, sticky=W, pady=5, padx=10)
dateFrame = Frame(formContainer, bg='#FFF8EF')
dateFrame.grid(row=3, column=1, sticky=W, pady=5)

tglVar = StringVar(window)
tglVar.set("1")
tglMenu = OptionMenu(dateFrame, tglVar, *[f"{i}" for i in range(1, 32)])
tglMenu.config(bg='#b6c8df', fg='#3f49a5')
tglMenu['menu'].config(font=('Tw Cen MT', 10), fg='#3f49a5', bg='#FFF8EF')
tglMenu.pack(side=LEFT)

blnVar = StringVar(window)
blnVar.set("1")
blnMenu = OptionMenu(dateFrame, blnVar, *[f"{i}" for i in range(1, 13)])
blnMenu.config(bg='#b6c8df', fg='#3f49a5', padx=5)
blnMenu['menu'].config(font=('Tw Cen MT', 10), fg='#3f49a5', bg='#FFF8EF')
blnMenu.pack(side=LEFT, padx=5)

thnVar = StringVar(window)
thnVar.set("2026")
thnMenu = OptionMenu(dateFrame, thnVar, *[str(i) for i in range(1990, 2027)])
thnMenu.config(bg='#b6c8df', fg='#3f49a5')
thnMenu['menu'].config(font=('Tw Cen MT', 10), fg='#3f49a5', bg='#FFF8EF')
thnMenu.pack(side=LEFT)

Label(formContainer, text="Departemen :", font=('Tw Cen MT', 12), fg='#3F49A5', bg='#FFF8EF').grid(row=4, column=0, sticky=W, pady=5, padx=10)
deptVar = StringVar(window)
deptVar.set("Finance & Accounting")
deptMenu = OptionMenu(formContainer, deptVar, "Finance & Accounting", "Sales & Marketing", "Human Resources", "Research & Development", "Legal & Administration", "Operations") 
deptMenu.config(width=27, font=('Tw Cen MT', 10), bg='#b6c8df', fg='#3f49a5')
deptMenu['menu'].config(font=('Tw Cen MT', 10), fg='#3f49a5', bg='#FFF8EF')
deptMenu.grid(row=4, column=1, sticky=W, pady=5)

Label(formContainer, text="Metode Pembayaran :", font=('Tw Cen MT', 12), fg='#3F49A5', bg='#FFF8EF').grid(row=5, column=0, sticky=W, pady=5, padx=10)
payVar = StringVar(window)
payVar.set("Cash")
payMenu = OptionMenu(formContainer, payVar, "Cash", "Transfer Bank", "Kartu Perusahaan", "Giro", "QRIS", "E-Wallet")
payMenu.config(width=27, font=('Tw Cen MT', 10), bg='#b6c8df', fg='#3f49a5')
payMenu['menu'].config(font=('Tw Cen MT', 10), fg='#3f49a5', bg='#FFF8EF')
payMenu.grid(row=5, column=1, sticky=W, pady=5)

Label(formContainer, text="No. Invoice :", font=('Tw Cen MT', 12), fg='#3F49A5', bg='#FFF8EF').grid(row=6, column=0, sticky=W, pady=5, padx=10)
invoiceEntry = Entry(formContainer, font=('Tw Cen MT', 12), width=30)
invoiceEntry.grid(row=6, column=1, sticky=W, pady=5)

Label(formContainer, text="Notes :", font=('Tw Cen MT', 12), fg='#3F49A5', bg='#FFF8EF').grid(row=7, column=0, sticky=W, pady=5, padx=10)
notesEntry = Entry(formContainer, font=('Tw Cen MT', 12), width=30)
notesEntry.grid(row=7, column=1, sticky=W, pady=5)

actionFrame = Frame(frameAddtrans, bg='#FFF8EF')
actionFrame.pack(pady=15)

simpanBt = Button(actionFrame, text="Simpan Transaksi", font=('Tw Cen MT', 12, 'bold'), bg='#b6c8df', fg='#3f49a5', command=handleaddTrans)
simpanBt.pack(side=LEFT, padx=20)

batalBt = Button(actionFrame, text="Kembali", command=backfromAdd, font=('Tw Cen MT', 12), bg='#b6c8df', fg='#3f49a5')
batalBt.pack(side=LEFT, padx=20)

updateKategoriOptions()

# ==========================================
# PEMBUATAN FRAME LIHAT TRANSAKSI
# ==========================================
frameViewtrans = Frame(window, bg='#FFF8EF')

titleView = Label(frameViewtrans, text="Daftar Transaksi Perusahaan", font=('Tw Cen MT', 20, 'bold'), fg='#3F49A5', bg='#FFF8EF')
titleView.pack(pady=10)

style = ttk.Style()
style.theme_use("default") 

style.configure("Treeview.Heading",
                background="#b6c8df",       
                foreground="#3F49A5",      
                font=('Tw Cen MT', 11, 'bold'), 
                relief="flat")
style.map("Treeview.Heading", background=[('active', '#b6c8df')]) 

style.configure("Treeview",
                background="#FFF8EF",       
                fieldbackground="#FFF8EF",  
                foreground="#3F49A5",
                font=('Tw Cen MT', 10),       
                rowheight=25)               

style.map("Treeview",
          background=[('selected', '#3F49A5')], 
          foreground=[('selected', '#b6c8df')]) 

tableContainer = Frame(frameViewtrans, bg='#FFF8EF')
tableContainer.pack(pady=10, padx=20, fill="both", expand=True)

scrollX = Scrollbar(tableContainer, orient=HORIZONTAL)
scrollY = Scrollbar(tableContainer, orient=VERTICAL)

cols = ("Tanggal", "Tipe", "Kategori", "Jumlah", "Departemen", "Metode", "Invoice", "Notes")

tableTrans = ttk.Treeview(
    tableContainer, 
    columns=cols, 
    show="headings", 
    selectmode="browse",
    xscrollcommand=scrollX.set, 
    yscrollcommand=scrollY.set
)

scrollX.config(command=tableTrans.xview)
scrollY.config(command=tableTrans.yview)

scrollX.pack(side=BOTTOM, fill="x")
scrollY.pack(side=RIGHT, fill="y")
tableTrans.pack(side=LEFT, fill="both", expand=True)

columnWidth = {
    "Tanggal": 100, 
    "Tipe": 100, 
    "Kategori": 180, 
    "Jumlah": 120, 
    "Departemen": 160, 
    "Metode": 120, 
    "Invoice": 150, 
    "Notes": 250
}

for k in cols:
    tableTrans.heading(k, text=k)
    tableTrans.column(k, width=columnWidth[k], minwidth=100, anchor=W if k in ["Notes", "Kategori"] else CENTER)

btBackfromview = Button(frameViewtrans, text="Kembali", command=backfromView, font=('Tw Cen MT', 12), bg='#b6c8df', fg='#3f49a5')
btBackfromview.pack(pady=15)

# ==========================================
# PEMBUATAN FRAME REKAP TRANSAKSI
# ==========================================
frameRecap = Frame(window, bg='#FFF8EF')

titleRecap = Label(frameRecap, text="Rekapitulasi Keuangan Perusahaan", font=('Tw Cen MT', 20, 'bold'), fg='#3F49A5', bg='#FFF8EF')
titleRecap.pack(pady=(20, 10))

boxSum = LabelFrame(frameRecap, text=" Ringkasan Saldo ", font=('Tw Cen MT', 12, 'bold'), fg='#3F49A5', bg='#FFF8EF', padx=20, pady=20)
boxSum.pack(pady=20, padx=50, fill="x")

Label(boxSum, text="Total Pemasukan :", font=('Tw Cen MT', 13), fg='#3F49A5', bg='#FFF8EF').grid(row=0, column=0, sticky=W, pady=10)
valIncome = Label(boxSum, text="Rp 0", font=('Tw Cen MT', 13, 'bold'), bg='#FFF8EF')
valIncome.grid(row=0, column=1, sticky=E, padx=(50, 0))

Label(boxSum, text="Total Pengeluaran :", font=('Tw Cen MT', 13), fg='#3F49A5', bg='#FFF8EF').grid(row=1, column=0, sticky=W, pady=10)
valExpense = Label(boxSum, text="Rp 0", font=('Tw Cen MT', 13, 'bold'), bg='#FFF8EF')
valExpense.grid(row=1, column=1, sticky=E, padx=(50, 0))

divider = Frame(boxSum, height=2, bd=1, relief=SUNKEN, bg='#b6c8df')
divider.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

Label(boxSum, text="Saldo Saat Ini :", font=('Tw Cen MT', 14, 'bold'), fg='#3F49A5', bg='#FFF8EF').grid(row=3, column=0, sticky=W, pady=10)
valSaldo = Label(boxSum, text="Rp 0", font=('Tw Cen MT', 14, 'bold'), bg='#FFF8EF')
valSaldo.grid(row=3, column=1, sticky=E, padx=(50, 0))

boxSum.columnconfigure(0, weight=1)
boxSum.columnconfigure(1, weight=1)

btBackfromrec = Button(frameRecap, text="Kembali", command=backfromRec, font=('Tw Cen MT', 12), bg='#b6c8df', fg='#3f49a5')
btBackfromrec.pack(pady=10)

# ==========================================
# LOGIKA AUTO-LOGIN
# ==========================================
try:
    with open("sessionToken.txt", "r") as file:
        savedToken = file.read().strip()
        
    if savedToken:
        print("Sudah pernah log in - langsung menuju home...")
        sesToken = savedToken
        frameInit.pack_forget()  
        goToHome()          
except FileNotFoundError:
    print("Belum pernah log in - masuk ke init...")

window.mainloop()
