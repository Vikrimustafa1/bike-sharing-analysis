# 🚲 Bike Sharing Dashboard

**Proyek Akhir — Belajar Analisis Data dengan Python (Dicoding)**

| Field | Info |
|-------|------|
| **Nama** | Muhammad Vikri Mustafa |
| **Email** | vikrimustafa24@gmail.com |
| **ID Dicoding** | muhammad_mustafaw3cb |
| **Dataset** | Bike Sharing Dataset (Capital Bikeshare, Washington D.C. 2011–2012) |

---

## 📂 Struktur Direktori

```
submission/
├── dashboard/
│   ├── main_data_day.csv          ← Data harian yang sudah dibersihkan
│   ├── main_data_hour.csv         ← Data per jam yang sudah dibersihkan
│   └── dashboard.py               ← Aplikasi Streamlit
├── data/
│   ├── day.csv                    ← Dataset harian (raw)
│   ├── hour.csv                   ← Dataset per jam (raw)
│   └── Readme.txt                 ← Dokumentasi dataset asli
├── notebook.ipynb                 ← Notebook analisis data lengkap
├── requirements.txt               ← Daftar library yang digunakan
└── README.md                      ← File ini
```

---

## 🔍 Pertanyaan Bisnis

1. **Pertanyaan 1 (Musim & Cuaca):**  
   Bagaimana rata-rata jumlah peminjaman sepeda harian berdasarkan musim (*season*) dan kondisi cuaca (*weathersit*) selama tahun 2011–2012, dan kombinasi musim-cuaca manakah yang menghasilkan rata-rata penyewaan tertinggi?

2. **Pertanyaan 2 (Pola Per Jam):**  
   Pada jam berapa puncak penggunaan sepeda berbagi terjadi pada hari kerja (*working day*) dibandingkan hari libur/akhir pekan sepanjang tahun 2011–2012, dan bagaimana pola ini mencerminkan perilaku pengguna kasual vs pengguna terdaftar?

---

## 🛠️ Cara Menjalankan Dashboard (Lokal)

### 1. Clone atau ekstrak folder proyek

```bash
unzip submission.zip
cd submission
```

### 2. Buat virtual environment (opsional, disarankan)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install semua dependensi

```bash
pip install -r requirements.txt
```

### 4. Jalankan dashboard Streamlit

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan otomatis terbuka di browser pada alamat:  
👉 **http://localhost:8501**

---

## 📦 Dependensi Utama

| Library | Versi | Fungsi |
|---------|-------|--------|
| `pandas` | 2.2.2 | Manipulasi dan analisis data |
| `numpy` | 1.26.4 | Komputasi numerik |
| `matplotlib` | 3.9.0 | Visualisasi data statis |
| `seaborn` | 0.13.2 | Visualisasi statistik |
| `scipy` | 1.13.1 | Analisis statistik |
| `streamlit` | 1.35.0 | Framework dashboard interaktif |

---

## 📊 Fitur Dashboard

- **Filter Interaktif:** Filter berdasarkan tahun, musim, dan kondisi cuaca
- **Kartu Metrik:** Ringkasan statistik kunci secara real-time
- **Tab Q1 (Musim & Cuaca):** Bar chart perbandingan, heatmap kombinasi musim×cuaca
- **Tab Q2 (Pola Per Jam):** Line chart pola jam, area chart kasual vs terdaftar
- **Tab Tren Waktu:** Tren bulanan, distribusi per hari dalam seminggu, scatter plot suhu
- **Tab Analisis Lanjutan:** Clustering binning berdasarkan kuartil, profil klaster, komposisi musim

---

## 💡 Temuan Utama

- **Musim Gugur (Fall)** memiliki rata-rata penyewaan tertinggi (~5.644/hari), 116% lebih tinggi dari Spring
- **Cuaca cerah** mendorong penyewaan hingga 170% lebih tinggi dibandingkan hujan/salju ringan
- Hari kerja: pola **bimodal komuter** (puncak 08:00 & 17:00)
- Hari libur: pola **unimodal rekreasi** (puncak 13:00)
- **Suhu** berkorelasi positif kuat dengan penyewaan (r ≈ 0.63)

---

## 🙏 Lisensi Dataset

Fanaee-T, Hadi, and Gama, Joao — *"Event labeling combining ensemble detectors and background knowledge"*, Progress in Artificial Intelligence, Springer Berlin Heidelberg, 2013.
