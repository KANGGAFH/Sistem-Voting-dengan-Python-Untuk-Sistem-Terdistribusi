import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import mysql.connector
import hashlib
import matplotlib.pyplot as plt

# ---------------------- Hash Password ----------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------------- GUI Modern ----------------------
class VotingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Voting")
        self.root.geometry("420x520")

        db_hosts = ["172.10.11.78", "172.10.xxx.xxx", "192.168.xxx.xxx", "192.168.xxx.xxx"]  # Tambahkan IP cadangan di sini
        self.db = None
        self.cursor = None

        for host in db_hosts:
            try:
                self.db = mysql.connector.connect(
                    host=host,
                    user="xxx", #masukkan user
                    password="xxx", #password
                    database="xxx" #databse yang digunakkan
                )
                self.cursor = self.db.cursor()
                print(f"Terhubung ke server di {host}")
                break
            except mysql.connector.Error as err:
                print(f"Gagal terhubung ke {host}: {err}")

        if self.db is None:
            messagebox.showerror("Koneksi Gagal", "Gagal terhubung ke semua server.")
            root.destroy()
            return

        self.show_login_screen()


    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_frame()
        ttk.Label(self.root, text="Login Voting", font=("Segoe UI", 20, "bold")).pack(pady=30)

        ttk.Label(self.root, text="Username").pack(anchor="w", padx=40)
        username_entry = ttk.Entry(self.root, width=30)
        username_entry.pack(pady=5)

        ttk.Label(self.root, text="Password").pack(anchor="w", padx=40)
        password_entry = ttk.Entry(self.root, width=30, show="*")
        password_entry.pack(pady=5)

        def login():
            username = username_entry.get()
            password = hash_password(password_entry.get())
            self.cursor.execute("SELECT id, password, role FROM users WHERE username = %s", (username,))
            result = self.cursor.fetchone()

            if result and result[1] == password:
                user_id, _, role = result
                if role == 'admin':
                    self.admin_menu()
                else:
                    self.voter_menu(user_id)
            else:
                messagebox.showerror("Gagal", "Username atau password salah")

        ttk.Button(self.root, text="Login", command=login, bootstyle="success").pack(pady=10)
        ttk.Button(self.root, text="Daftar Akun Voter", command=self.show_register_screen, bootstyle="info").pack(pady=5)

    def show_register_screen(self):
        self.clear_frame()
        ttk.Label(self.root, text="Daftar Voter", font=("Segoe UI", 20, "bold")).pack(pady=30)

        ttk.Label(self.root, text="Username").pack(anchor="w", padx=40)
        username_entry = ttk.Entry(self.root, width=30)
        username_entry.pack(pady=5)

        ttk.Label(self.root, text="Password").pack(anchor="w", padx=40)
        password_entry = ttk.Entry(self.root, width=30, show="*")
        password_entry.pack(pady=5)

        def register():
            username = username_entry.get()
            password = hash_password(password_entry.get())
            try:
                self.cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, 'voter')", (username, password))
                self.db.commit()
                messagebox.showinfo("Sukses", "Registrasi berhasil!")
                self.show_login_screen()
            except mysql.connector.IntegrityError:
                messagebox.showerror("Gagal", "Username sudah digunakan.")

        ttk.Button(self.root, text="Daftar", command=register, bootstyle="primary").pack(pady=10)
        ttk.Button(self.root, text="Kembali", command=self.show_login_screen, bootstyle="danger").pack()

    def admin_menu(self):
        self.clear_frame()
        ttk.Label(self.root, text="Menu Admin", font=("Segoe UI", 18, "bold")).pack(pady=20)

        def buat_pemilihan():
            nama = simple_input("Nama Pemilihan")
            if nama:
                self.cursor.execute("UPDATE elections SET active = 0")
                self.cursor.execute("INSERT INTO elections (name, active) VALUES (%s, 1)", (nama,))
                self.db.commit()
                messagebox.showinfo("Sukses", "Pemilihan dibuat dan diaktifkan.")

        def tambah_kandidat():
            nama = simple_input("Nama Kandidat")
            if nama:
                self.cursor.execute("SELECT id FROM elections WHERE active = 1 LIMIT 1")
                result = self.cursor.fetchone()
                if result:
                    eid = result[0]
                    self.cursor.execute("INSERT INTO candidates (name, election_id) VALUES (%s, %s)", (nama, eid))
                    self.db.commit()
                    messagebox.showinfo("Sukses", "Kandidat ditambahkan.")
                else:
                    messagebox.showwarning("Peringatan", "Tidak ada pemilihan aktif.")

        def lihat_hasil():
            self.cursor.execute("""
                SELECT c.name, COUNT(v.id)
                FROM votes v
                JOIN candidates c ON v.candidate_id = c.id
                GROUP BY c.name
            """)
            data = self.cursor.fetchall()
            if data:
                labels, counts = zip(*data)
                plt.figure(figsize=(5, 5))
                plt.pie(counts, labels=labels, autopct='%1.1f%%')
                plt.title("Hasil Voting")
                plt.show()
            else:
                messagebox.showinfo("Info", "Belum ada suara.")

        ttk.Button(self.root, text="Buat Pemilihan Baru", command=buat_pemilihan, bootstyle="success").pack(pady=5)
        ttk.Button(self.root, text="Tambah Kandidat", command=tambah_kandidat, bootstyle="info").pack(pady=5)
        ttk.Button(self.root, text="Lihat Hasil Voting", command=lihat_hasil, bootstyle="warning").pack(pady=5)
        ttk.Button(self.root, text="Logout", command=self.show_login_screen, bootstyle="danger").pack(pady=20)

    def voter_menu(self, user_id):
        self.clear_frame()
        self.cursor.execute("SELECT has_voted FROM users WHERE id = %s", (user_id,))
        if self.cursor.fetchone()[0]:
            messagebox.showinfo("Info", "Kamu sudah memberikan suara.")
            self.show_login_screen()
            return

        self.cursor.execute("SELECT id FROM elections WHERE active = 1 LIMIT 1")
        eid = self.cursor.fetchone()
        if not eid:
            messagebox.showwarning("Peringatan", "Belum ada pemilihan aktif.")
            self.show_login_screen()
            return

        eid = eid[0]
        self.cursor.execute("SELECT id, name FROM candidates WHERE election_id = %s", (eid,))
        candidates = self.cursor.fetchall()

        ttk.Label(self.root, text="Pilih Kandidat", font=("Segoe UI", 16, "bold")).pack(pady=20)

        pilihan = ttk.IntVar()
        for cid, nama in candidates:
            ttk.Radiobutton(self.root, text=nama, variable=pilihan, value=cid).pack(anchor='w', padx=40)

        def submit():
            cid = pilihan.get()
            if cid:
                self.cursor.execute("INSERT INTO votes (voter_id, candidate_id) VALUES (%s, %s)", (user_id, cid))
                self.cursor.execute("UPDATE users SET has_voted = 1 WHERE id = %s", (user_id,))
                self.db.commit()
                messagebox.showinfo("Sukses", "Voting berhasil!")
                self.show_login_screen()
            else:
                messagebox.showwarning("Peringatan", "Pilih salah satu kandidat.")

        ttk.Button(self.root, text="Kirim Suara", command=submit, bootstyle="success").pack(pady=20)
        ttk.Button(self.root, text="Kembali", command=self.show_login_screen, bootstyle="danger").pack()

# ---------------------- Utility ----------------------
def simple_input(judul):
    popup = ttk.Toplevel()
    popup.title(judul)
    popup.geometry("300x150")
    ttk.Label(popup, text=judul, font=("Segoe UI", 12, "bold")).pack(pady=10)
    entry = ttk.Entry(popup, width=30)
    entry.pack(pady=5)
    val = ttk.StringVar()

    def submit():
        val.set(entry.get())
        popup.destroy()

    ttk.Button(popup, text="OK", command=submit, bootstyle="primary").pack(pady=10)
    popup.wait_window()
    return val.get()

# ---------------------- Run App ----------------------
if __name__ == "__main__":
    app_style = ttk.Style("flatly")  # Ganti ke tema lain: darkly, cyborg, superhero
    root = app_style.master
    app = VotingApp(root)
    root.mainloop()
