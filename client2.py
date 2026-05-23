import tkinter as frame
from tkinter import font

root = frame.Tk()
# Mengambil seluruh font yang terdaftar di OS laptopmu
seluruh_font = list(font.families())
seluruh_font.sort()

for f in seluruh_font:
    print(f)