from tkinter import *
import c2_security
import c2_network

def logIn():
    print("Membuka page log in... ")
    frameInit.pack_forget()
    frameLogin.pack(fill="both", expand=True)

def signUp():
    print("Membuka page sign up...")
    frameInit.pack_forget()
    frameSignup.pack(fill="both", expand=True)

def loggingIn():
    print("mengecek validasi data")
    user = unameEntry.get()
    pwd = pwEntry.get()
    pin = pinEntry.get()
    
    if not user or not pwd or not pin:
        errorLabel.config(text="Semua kolom wajib diisi!", fg="#ab3730")
        return
    if len(user) < 4 or len(user) > 30:
        errorLabel.config(text="Username harus 4-30 karakter!", fg="#ab3730")
        return
    if len(pwd) < 8 or len(pwd) > 64:
        errorLabel.config(text="Password harus 8-64 karakter!", fg="#ab3730")
        return
    if len(pin) < 4 or len(pin) > 8 or not pin.isdigit():
        errorLabel.config(text="PIN harus 4-8 digit angka!", fg="#ab3730")
        return
    errorLabel.config(text="Memvalidasi data...", fg="#3f49a5")
    window.update()
    payload = {
        "username": user, 
        "password": pwd,
        "pin": pin
    }
    respon = c2_network.sendSocket("login", payload)
    
    if respon.get("status") == "success":
        errorLabel.config(text="Login Berhasil!", fg="green")
        return respon["data"]["session_token"]
    else:
        errorMessage = respon.get("message", "Gagal log in.")
        errorLabel.config(text=errorMessage, fg="#ab3730")
        return None

def signingUp():
    user = unameSEntry.get()
    pwd = pwSEntry.get()
    pin = pinSEntry.get()
    
    if not user or not pwd or not pin:
        errorSLabel.config(text="Semua kolom wajib diisi!", fg="#ab3730")
        return
    if len(user) < 4 or len(user) > 30:
        errorSLabel.config(text="Username harus 4-30 karakter!", fg="#ab3730")
        return
    if len(pwd) < 8 or len(pwd) > 64:
        errorSLabel.config(text="Password harus 8-64 karakter!", fg="#ab3730")
        return
    if len(pin) < 4 or len(pin) > 8 or not pin.isdigit():
        errorSLabel.config(text="PIN harus 4-8 digit angka!", fg="#ab3730")
        return
        
    errorSLabel.config(text="Mendaftarkan akun...", fg="#3f49a5")
    window.update()
    payload = {
        "username": user, 
        "password": pwd, 
        "pin": pin        
    }
    
    respon = c2_network.sendSocket("register", payload)
    
    if respon.get("status") == "success":
        errorSLabel.config(text="Registrasi berhasil dilakukan.", fg="green")
        return True
    else:
        errorMessage = respon.get("message", "Registrasi gagal dilakukan.")
        errorSLabel.config(text=errorMessage, fg="#ab3730")
        return False


def backtoInit():
    frameLogin.pack_forget()
    frameInit.pack(fill="both", expand=True)

def backtoInitS():
    frameSignup.pack_forget()
    frameInit.pack(fill="both", expand=True)


window = Tk() #window awal
window.geometry("800x400")
window.title("Cuan Tracker")

logo = PhotoImage(file='logo_ct.png')
window.iconphoto(True,logo)

# ==========================================
# FRAME INITIAL 
# ==========================================
frameInit = Frame(window, bg='#fff8ef')

frameInit.pack(fill="both", expand=True)

window.config(background="#FFF8EF")

titleInit = Label(frameInit,
              text="Cuan Tracker",
              font=('Helvetica',40,'bold'),fg='#3F49A5',bg='#FFF8EF',
              image=logo,
              compound='bottom'
              )
titleInit.pack(pady=10)

loginBt = Button(frameInit, text="Log In")
loginBt.config(command=logIn)
loginBt.config(font=('Helvetica',15, 'bold'))
loginBt.config(bg='#b6c8df')
loginBt.config(fg='#3f49a5')
loginBt.config(activebackground='#3f49a5')
loginBt.config(activeforeground='#b6c8df')
loginBt.pack()

signupBt = Button(frameInit, text="Sign Up")
signupBt.config(command=signUp)
signupBt.config(font=('Helvetica',15, 'bold'))
signupBt.config(bg='#b6c8df')
signupBt.config(fg='#3f49a5')
signupBt.config(activebackground='#3f49a5')
signupBt.config(activeforeground='#b6c8df')
signupBt.pack(pady=10)


# ==========================================
# FRAME LOG IN
# ==========================================
frameLogin = Frame(window, bg='#FFF8EF')
titleLogin = Label(frameLogin, text="Log In", font=('Helvetica', 25, 'bold'), fg='#3F49A5', bg='#FFF8EF')
titleLogin.pack(pady=10)

errorLabel = Label(frameLogin, text="", font=('Helvetica', 8, 'bold'), bg='#FFF8EF')
errorLabel.pack(pady=5)

unameLabel = Label(frameLogin, text="Username :", font=('Helvetica', 15), fg='#3F49A5', bg='#FFF8EF')
unameLabel.pack(pady=(5,0))
unameEntry = Entry(frameLogin, font=('Helvetica', 15), width=30)
unameEntry.pack(pady=5)

pwLabel = Label(frameLogin, text="Password :", font=('Helvetica', 15), fg='#3F49A5', bg='#FFF8EF')
pwLabel.pack(pady=(5,0))
pwEntry = Entry(frameLogin, font=('Helvetica', 15), width=64, show="•")
pwEntry.pack(pady=5)

pinLabel = Label(frameLogin, text="PIN Perusahaan :", font=('Helvetica', 15), fg='#3F49A5', bg='#FFF8EF')
pinLabel.pack(pady=(5,0))
pinEntry = Entry(frameLogin, font=('Helvetica', 15), width=8, show="•")
pinEntry.pack(pady=5)

frameBt = Frame(frameLogin, bg='#FFF8EF')
frameBt.pack(pady=10)

submitBt = Button(frameBt, text="Masuk", font=('Helvetica', 12, 'bold'), bg='#b6c8df', fg='#3f49a5', command=loggingIn)
submitBt.pack(side=LEFT, padx=30)

backBt = Button(frameBt, text="Kembali", font=('Helvetica', 12), bg='#b6c8df', fg='#3f49a5', command=backtoInit)
backBt.pack(side=LEFT, padx=20)

# ==========================================
# FRAME SIGN UP
# ==========================================
frameSignup = Frame(window, bg='#FFF8EF')
titleSignup = Label(frameSignup, text="Sign Up", font=('Helvetica', 25, 'bold'), fg='#3F49A5', bg='#FFF8EF')
titleSignup.pack(pady=10)

errorSLabel = Label(frameSignup, text="", font=('Helvetica', 8, 'bold'), bg='#FFF8EF')
errorSLabel.pack(pady=5)

unameSLabel = Label(frameSignup, text="Username :", font=('Helvetica', 15), fg='#3F49A5', bg='#FFF8EF')
unameSLabel.pack(pady=(5,0))
unameSEntry = Entry(frameSignup, font=('Helvetica',15), width=30)
unameSEntry.pack(pady=5)

pwSLabel = Label(frameSignup, text="Password :", font=('Helvetica', 15), fg='#3F49A5', bg='#FFF8EF')
pwSLabel.pack(pady=(5,0))
pwSEntry = Entry(frameSignup, font=('Helvetica', 15), width=64, show="•")
pwSEntry.pack(pady=5)

pinSLabel = Label(frameSignup, text="PIN Perusahaan :", font=('Helvetica', 15), fg='#3F49A5', bg='#FFF8EF')
pinSLabel.pack(pady=(5,0))
pinSEntry = Entry(frameSignup, font=('Helvetica', 15), width=8, show="•")
pinSEntry.pack(pady=5)


frameSBt = Frame(frameSignup, bg='#FFF8EF')
frameSBt.pack(pady=10)

submitSBt = Button(frameSBt, text="Masuk", font=('Helvetica', 12, 'bold'), bg='#b6c8df', fg='#3f49a5', command=signingUp)
submitSBt.pack(side=LEFT, padx=30)

backSBt = Button(frameSBt, text="Kembali", font=('Helvetica', 12), bg='#b6c8df', fg='#3f49a5', command=backtoInitS)
backSBt.pack(side=LEFT, padx=20)

window.mainloop()