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