# 🗳️ Sistem Voting dengan Python untuk Sistem Terdistribusi

Proyek ini merupakan implementasi **aplikasi voting digital** berbasis Python yang dirancang untuk berjalan dalam **arsitektur sistem terdistribusi**. Aplikasi ini memungkinkan pengguna untuk memberikan suara secara aman dan terstruktur, dilengkapi dengan peran admin, pemilih, dan pengelolaan pemilu.

## 📌 Fitur Utama

- 🔐 Login dengan peran `admin` dan `voter`
- ✅ Pemilih hanya bisa memberikan suara sekali
- 🗂️ Admin dapat mengelola:
  - Pemilu (Election)
  - Kandidat (Candidate)
  - Pemilih (Voter)
- 📊 Rekapitulasi hasil voting
- 🖥️ Sistem siap untuk dijalankan dalam lingkungan terdistribusi (multi-server)

## 🗄️ Struktur Database (MariaDB)

### Tabel: `users`
| Field       | Type           | Keterangan                   |
|-------------|----------------|------------------------------|
| id          | int(11)        | Primary key, auto_increment |
| username    | varchar(50)    | Unik                         |
| password    | varchar(255)   | Hash password                |
| role        | enum           | `'admin'` atau `'voter'`     |
| has_voted   | tinyint(1)     | Status apakah sudah memilih |

### Tabel: `elections`
| Field     | Type          | Keterangan                   |
|-----------|---------------|------------------------------|
| id        | int(11)       | Primary key, auto_increment |
| name      | varchar(100)  | Nama pemilu                  |
| active    | tinyint(1)    | Apakah pemilu sedang aktif   |

### Tabel: `candidates`
| Field       | Type         | Keterangan                        |
|-------------|--------------|-----------------------------------|
| id          | int(11)      | Primary key, auto_increment       |
| name        | varchar(100) | Nama kandidat                     |
| election_id | int(11)      | Foreign key → elections(id)       |

### Tabel: `votes`
| Field        | Type      | Keterangan                        |
|--------------|-----------|-----------------------------------|
| id           | int(11)   | Primary key, auto_increment       |
| voter_id     | int(11)   | Foreign key → users(id)           |
| candidate_id | int(11)   | Foreign key → candidates(id)      |

## 🛠️ Teknologi yang Digunakan

- Python
- Ubuntu Server
- Flask (untuk API/backend)
- MariaDB / MySQL
- Sistem Terdistribusi (master-slave deployment)
- Tkinter untuk antarmuka GUI
