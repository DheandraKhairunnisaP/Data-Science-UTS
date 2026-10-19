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
│   ├── 02_annotation_and_split.ipynb   # tahap berikutnya
│   └── 03_train_evaluate_ner.ipynb     # tahap berikutnya
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
