# Mangan" Solo

## Nama-nama Anggota Kelompok

- Muttaqin Muzakkir: 2306207101
- Fadiansah Feryan Fatha: 2306275185
- Delya Ardiyanti: 2306245586
- Asyer Samuel Marpaung: 2306165925
- Ali Al Uraydhi: 2306275992
- Crysandya Vic Rajendra: 2306165622

---

## Deskripsi Aplikasi

### Jelajahi Kelezatan Kuliner Solo dengan **Mangan Solo**—Hemat dan Lezat!

Tahukah Anda bahwa kota Solo atau yang juga dikenal sebagai Surakarta merupakan surga kuliner yang menawarkan berbagai makanan khas yang memikat selera dengan harga terjangkau? Dari gurihnya Nasi Liwet hingga lezatnya Selat Solo, semua informasi restoran tersedia dengan harga yang ramah di kantong di **Mangan Solo**.

**Mangan Solo** adalah aplikasi pencarian makanan khas Solo yang dirancang untuk membantu pelanggan menemukan dan menikmati hidangan-hidangan terbaik kota batik ini dengan mudah dan ekonomis. Dengan **Mangan Solo**, pengalaman kuliner pelanggan akan lebih praktis dan menyenangkan, serta lebih hemat!

### Asal Usul dan Tujuan Mangan Solo

Nama "Mangan Solo" berasal dari kata "mangan" yang dalam bahasa Jawa berarti makan, mencerminkan kekayaan dan keunikan kuliner Solo. Terinspirasi oleh kekhasan dan keekonomisan makanan di Solo, kelompok kami ingin menciptakan sebuah platform yang tidak hanya memudahkan pengunjung dari luar daerah untuk mendapatkan informasi terkini tentang kuliner di Solo tetapi juga memberi kesempatan bagi pemilik restoran lokal untuk memasarkan restoran mereka. **Mangan Solo** dirancang sebagai jembatan antara pencinta kuliner dan pelaku usaha kuliner di Solo, memperkaya pengalaman kuliner sambil memperkenalkan budaya lokal yang autentik kepada dunia.

---

## Fitur Utama

- **Pencarian Terperinci**: Gunakan search bar untuk mencari berdasarkan nama hidangan, atau filter hasil pencarian pelanggan berdasarkan kategori makanan, lokasi, atau rentang harga. Temukan makanan khas Solo yang sesuai dengan anggaran dan selera pelanggan.

- **Ulasan**: Fitur ulasan memberi kesempatan kepada pelanggan untuk memberi komentar dan memberikan rating berbintang pada restoran atau makanan. Setiap ulasan memungkinkan pelanggan untuk menulis judul pendek, deskripsi yang lebih mendetail, dan memberi rating antara 1 hingga 5 untuk menilai mutu. Fitur ini juga memungkinkan untuk mengunggah gambar yang melengkapi narasi pelanggan, serta menyukai ulasan yang bermanfaat.

- **Tambah Restoran**: Fitur ini memungkinkan pemilik restoran untuk mendaftarkan restoran mereka, mengisi informasi penting seperti nama restoran, lokasi, jenis makanan, rentang harga, dan foto-foto fasilitas. Restoran akan lebih mudah ditemukan dalam pencarian oleh pelanggan.

- **Berita dan Promosi**: Menampilkan artikel, update, dan promosi terkini terkait restoran. Fitur ini memudahkan restoran untuk memasarkan restoran mereka, serta memberikan informasi terbaru kepada pelanggan mengenai penawaran khusus atau menu baru.

- **Thread Diskusi**: Pelanggan dan pemilik restoran dapat berinteraksi dalam thread diskusi, berbagi rekomendasi, pengalaman makan, tips kuliner Solo, dan informasi lainnya.

---

## Manfaat Aplikasi

1. **Kemudahan Akses Kuliner**: Pengguna dapat menemukan berbagai pilihan kuliner khas Solo dengan mudah melalui pencarian yang disediakan.
2. **Interaksi dan Informasi Terkini**: Pengguna dapat mendapatkan informasi promosi dan event terbaru langsung di aplikasi.
3. **Meningkatkan Visibilitas dan Interaksi**: Pemilik restoran dapat memperluas visibilitas dan mendapatkan feedback dari pengguna melalui ulasan.
4. **Efisiensi Biaya dan Waktu**: Informasi yang lengkap menghemat waktu dan biaya dalam menemukan tempat makan yang sesuai.
5. **Konektivitas dengan Komunitas Kuliner**: Pengguna bisa berbagi tips, berdiskusi, dan membangun komunitas pencinta kuliner hemat.

---

## Daftar Modul yang Akan Diimplementasikan

### Modul Restoran - Atha

Modul ini merupakan subjek utama website yang akan dimanipulasi oleh pemilik bisnis. Restoran memiliki beberapa field: Nama Restoran, Kecamatan, Alamat, Nama Makanan, Jenis Makanan, Harga, dan foto yang disimpan di dalam database. Pemilik bisnis yang terdaftar dapat memiliki tepat satu restoran. Restoran akan diperlihatkan ke Guest dan Customer. Customer dapat berinteraksi dengan modul ini dalam bentuk bookmark dan review.

### Modul Berita - Asyer

Modul ini memungkinkan pemilik bisnis untuk membuat dan mempublikasikan berita terkait restoran mereka. Berita ini dapat berisi informasi promosi, event, menu baru, atau update lainnya. Modul ini menjadi media promosi efektif yang membantu meningkatkan interaksi antara pemilik restoran dan pengguna aplikasi (Customer maupun Guest).

### Modul Review - Adel

Modul ini memungkinkan pelanggan memberikan ulasan terhadap pengalaman mereka di restoran. Fitur ini mencakup atribut seperti identitas pengguna (Customer), judul ulasan (CharField), tanggal ulasan (DateField), waktu ulasan (DateTimeField), dan penilaian (IntegerField). Sistem Like() memungkinkan pelanggan melihat reaksi orang lain terhadap ulasan yang diberikan.

### Modul Thread - Muttaqin

Fitur ini adalah platform diskusi yang memungkinkan semua pengguna untuk berinteraksi dan berbagi pendapat tentang topik terkait kuliner Solo. Fitur ini memperkuat komunitas dalam aplikasi.

### Modul Bookmark - Ali

Fitur ini memungkinkan pengguna menyimpan restoran favorit mereka untuk diakses kembali di masa mendatang. Fitur ini dirancang untuk meningkatkan kenyamanan pengguna dalam mengelola daftar restoran yang ingin dikunjungi lagi atau direkomendasikan.

### Modul Profil - Vicky

Modul ini mengelola informasi dan pengaturan pengguna. Profil pengguna dibagi menjadi dua jenis role: pelanggan dan pemilik restoran. Modul ini memungkinkan pengguna membuat, melihat, mengubah, dan menghapus akun.

---

## Role atau Peran Pengguna Aplikasi

### Guest

Guest adalah pengguna yang belum melakukan proses registrasi atau login. Mereka hanya dapat mengakses fitur-fitur umum yang bersifat "read-only". Akses Guest terbatas pada:

- **Read**:

  - Melihat daftar restoran.
  - Mengakses halaman review dan membaca ulasan.
  - Membaca berita yang diposting oleh pemilik restoran.

- **No Access**:
  - Tidak bisa memberikan ulasan atau rating.
  - Tidak bisa menyimpan restoran ke dalam bookmark.
  - Tidak bisa mengakses fitur pengelolaan restoran atau profil.

---

### Customer

Customer adalah pengguna terdaftar yang memiliki akses penuh untuk berinteraksi dengan konten aplikasi. Akses Customer mencakup:

- **Create**:

  - Membuat ulasan dan penilaian (CRUD review).
  - Menyimpan restoran ke bookmark.
  - Berpartisipasi dalam thread diskusi.

- **Read**:

  - Menelusuri dan melihat daftar restoran.
  - Membaca ulasan, berita, dan thread.

- **Update**:

  - Memperbarui ulasan, profil, dan komentar.

- **Delete**:
  - Menghapus ulasan, bookmark, dan komentar di thread.

---

### Pemilik Restoran

Pemilik Restoran memiliki akses untuk membuat, membaca, memperbarui, dan menghapus restoran dan berita yang mereka buat. Akses Pemilik Restoran meliputi:

- **Create**:

  - Membuat restoran, berita, profil, dan thread.

- **Read**:

  - Melihat semua restoran, berita, review, dan thread.

- **Update**:

  - Memperbarui restoran, berita, profil, dan thread.

- **Delete**:
  - Menghapus restoran, berita, profil, dan thread.

---

## Sumber Initial Dataset

Dataset A07 PBP - UTS
Dataset kami merupakan hasil scraping dari Internet untuk menemukan makanan khas di kecamatan-kecamatan Surakarta.
[DATASET](https://docs.google.com/spreadsheets/d/1txREr6OPf12FaUS8rfti79dRXVMz9-th0x-sfVrwtws/edit?gid=0#gid=0)

---

## Tautan Deployment Aplikasi

[Deployment Mangan" Solo](http://muttaqin-muzakkir-utspbp.pbp.cs.ui.ac.id/)
