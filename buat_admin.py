import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style
from ttkbootstrap.widgets import Entry, Button, Label, Frame
import mysql.connector
import hashlib

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def tambah_admin():
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if not username or not password:
        messagebox.showwarning("Input Kosong", "Username dan Password tidak boleh kosong.")
        return

    hashed_pw = hash_password(password)

    try:
        conn = mysql.connector.connect(
            host="192.168.xxx.xxx", #ip host
            user="xxx", #user
            password="xxx", #password
            database="xxx" #database yang digunakan
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, 'admin')",
            (username, hashed_pw)
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Sukses", f"Admin '{username}' berhasil ditambahkan!")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
    except mysql.connector.Error as err:
        messagebox.showerror("Gagal", f"Gagal menambahkan admin.\nError: {err}")

# GUI
root = tk.Tk()
root.title("Tambah Admin Voting")
root.geometry("400x300")
root.resizable(False, False)

style = Style("flatly")  # Gaya modern: flatly, cyborg, morph, darkly, dll
style.configure("TButton", font=("Segoe UI", 11))
style.configure("TLabel", font=("Segoe UI", 11))

frame = Frame(root, padding=20)
frame.pack(expand=True)

Label(frame, text="Tambah Admin Baru", font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))

Label(frame, text="Username:").pack(anchor="w")
entry_username = Entry(frame, width=30)
entry_username.pack(pady=5)

Label(frame, text="Password:").pack(anchor="w")
entry_password = Entry(frame, width=30, show="*")
entry_password.pack(pady=5)

Button(frame, text="Tambah Admin", bootstyle="success", command=tambah_admin).pack(pady=20)

root.mainloop()
