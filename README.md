# Data-Science-UTS

Proyek UTS NLP: **Article Named-Entity Recognition (NER) Service**. Sistem menerima judul dan isi artikel, lalu mengembalikan entitas bernama beserta label dan posisi karakter melalui API serta antarmuka web.

## Mulai di Google Colab

1. Buka [Notebook 01 — Profiling Dataset](https://colab.research.google.com/github/DheandraKhairunnisaP/Data-Science-UTS/blob/main/notebooks/01_profiling_dataset.ipynb).
2. Jalankan sel dari atas ke bawah.
3. Unggah ZIP dataset dari dosen ketika diminta.
4. Unduh dan simpan ZIP hasil profiling. Jangan commit dataset mentah ke repository.
5. Setelah profiling dan audit duplikasi diperiksa, lanjut ke anotasi manual dan pembagian data.

## Pembagian kerja 3 anggota

- **Anggota 1 — Data dan anotasi:** profiling, audit kualitas data, pedoman label, anotasi span-level, dan dokumentasi sumber/ID artikel.
- **Anggota 2 — Model dan evaluasi:** baseline pretrained, training/adaptasi pipeline dengan anotasi kelompok, evaluasi precision/recall/F1, per-label metrics, dan analisis kesalahan.
- **Anggota 3 — Aplikasi dan pengujian:** API `POST /extract-entities`, antarmuka browser, validasi input, error handling, pengujian integrasi, requirements, dan README.

Ketiga anggota harus ikut memeriksa konsistensi anotasi. Test set dipisahkan berdasarkan identitas artikel dan tidak boleh digunakan untuk tuning model.

## Rencana struktur repository

```
.
├── README.md
├── .gitignore
├── notebooks/
│   ├── 01_profiling_dataset.ipynb
│   ├── 02_prepare_annotation.ipynb
│   ├── 03_train_evaluate_ner.ipynb
│   └── 05_run_role3_app_colab.ipynb
├── data/                               # data lokal; jangan commit dataset mentah
├── models/                             # artefak model; jangan commit file besar tanpa keputusan kelompok
├── app/                                # API dan antarmuka web
└── tests/                              # kasus uji otomatis
```

## Persyaratan inti dari studi kasus

- Masukan JSON berisi `title` dan `body`; keduanya harus string dan tidak kosong.
- Endpoint mengembalikan `text`, `label`, `start`, `end`, serta metadata model dan jumlah entitas.
- Model akhir harus dilatih/diadaptasi menggunakan anotasi dari data contoh; pretrained model hanya baseline.
- Evaluasi held-out test melaporkan exact-span precision, recall, F1 keseluruhan dan per label, perbandingan baseline-vs-trained, serta minimal tiga kesalahan.
- Minimal lima kasus uji otomatis/reproducible; README memuat instalasi, startup, contoh request/response, model, arsitektur, dan keterbatasan.

## Catatan data

Kolom `entities` pada CSV belum tentu merupakan anotasi gold-standard. Notebook profiling memeriksa apakah kolom ini terisi, tetapi anotasi final untuk evaluasi harus ditinjau manusia. Data artikel sumber tidak disalin ke repository.


## Notebook lanjutan

- [Notebook 01 — Profiling Dataset](https://colab.research.google.com/github/DheandraKhairunnisaP/Data-Science-UTS/blob/main/notebooks/01_profiling_dataset.ipynb)
- [Notebook 02 — Persiapan Anotasi](https://colab.research.google.com/github/DheandraKhairunnisaP/Data-Science-UTS/blob/main/notebooks/02_prepare_annotation.ipynb)
- [Notebook 03 — Training dan Evaluasi](https://colab.research.google.com/github/DheandraKhairunnisaP/Data-Science-UTS/blob/main/notebooks/03_train_evaluate_ner.ipynb)
- [Notebook 04 — API dan Web App](https://colab.research.google.com/github/DheandraKhairunnisaP/Data-Science-UTS/blob/main/notebooks/04_build_api_web_app.ipynb)

Jalankan notebook secara berurutan. Notebook 03 membutuhkan CSV anotasi yang sudah ditinjau manusia. Notebook 04 membutuhkan paket model hasil Notebook 03.


## Role 3 — API dan Web App

Source code aplikasi berada di:
- `app/main.py`: FastAPI, validasi input, dan inferensi model.
- `web/index.html`: halaman form dan tabel hasil.
- `tests/test_api.py`: delapan tes otomatis.
- `requirements.txt`: dependensi Python.
- `docs/role2_evaluation_audit.md`: catatan pemeriksaan konsistensi metrik yang dikirim Role 2.

### Menjalankan demo di Google Colab

Buka [Notebook 05 — Run Role 3 App](https://colab.research.google.com/github/DheandraKhairunnisaP/Data-Science-UTS/blob/main/notebooks/05_run_role3_app_colab.ipynb), lalu unggah paket `Role3_Article_NER_Service.zip` yang disertakan dalam hasil kerja kelompok. Notebook menjalankan test, memulai server, dan menampilkan tautan aplikasi.

### Menjalankan lokal

Pasang dependensi dengan `pip install -r requirements.txt`, pastikan model dari Role 2 diekstrak ke `models/ner_custom_v1/`, lalu jalankan `uvicorn app.main:app --host 127.0.0.1 --port 8000`. Buka `http://127.0.0.1:8000`. Jalankan tes dengan `python -m pytest -q`.

**Evaluasi model:** file deliverables Role 2 mempunyai ketidaksesuaian antara support metrik overall dan metrik per-label. Lihat `docs/role2_evaluation_audit.md`; angka per-label perlu dihitung ulang sebelum dilaporkan sebagai hasil final.
