# Catatan Presentasi UTS — Role 3 (API dan Web App)

## Ringkasan yang bisa disampaikan

"Bagian saya adalah implementasi layanan NER dalam bentuk aplikasi web. Backend dibuat dengan FastAPI dan menggunakan model spaCy `ner_custom_v1` dari tahap training. Pengguna memasukkan judul dan isi artikel, lalu backend menggabungkan keduanya, menjalankan model, dan mengembalikan entitas dalam JSON. Halaman web menampilkan teks entitas, label, serta posisi karakter start dan end."

## Demo langsung (urutan 2–3 menit)

1. Buka aplikasi dan tunjukkan kolom judul serta isi artikel.
2. Gunakan contoh:
   - Judul: `Malaysia and Maybank Announce New Plans`
   - Isi: `Maybank said the company would expand its services in Kuala Lumpur on October 22, 2026.`
3. Tekan **Analisis entitas**.
4. Tunjukkan hasil aktual pada model yang disediakan: Malaysia (GPE), Maybank (ORG), Maybank (ORG), Kuala Lumpur (GPE), October 22, 2026 (DATE). Prediksi bisa berubah jika model diganti.
5. Jelaskan bahwa `start` indeks awal inklusif, `end` indeks akhir eksklusif pada teks gabungan judul + newline + isi.
6. Buka `/docs` untuk endpoint `POST /extract-entities`.
7. Bila diminta pengujian, tunjukkan `python -m pytest -q`: 9 passed.

## Fungsi utama backend

- Memvalidasi `title` dan `body` sebagai string yang tidak kosong.
- Batas input: judul 500 karakter, isi 10.000 karakter.
- JSON rusak, field salah tipe, input kosong, dan input terlalu panjang ditolak dengan HTTP 400.
- Output JSON memuat `entities` dan `meta`.
- Setiap entitas memuat `text`, `label`, `start`, `end`.

## Bukti verifikasi aplikasi

- Model berhasil dimuat dengan spaCy 3.8.11 pada lingkungan pengujian.
- `GET /health`, `GET /`, `GET /model-info`, dan `GET /docs` memberikan HTTP 200.
- `POST /extract-entities` contoh menghasilkan HTTP 200 dan 5 entitas.
- Offset setiap hasil cocok dengan irisan teks gabungan.
- Sembilan unit/API tests lulus, juga setelah ZIP aplikasi diekstrak ulang.

## Catatan evaluasi model Role 2

Deliverables Role 2 melaporkan overall final-test precision ≈ 0.9506, recall ≈ 0.9854, dan F1 ≈ 0.9677. Namun, jumlah TP pada metrik per-label jika dijumlahkan jauh melampaui 410 entitas gold yang disebutkan notebook. Jadi tabel metrik per-label tidak konsisten dengan angka overall. Jika dosen bertanya, jelaskan bahwa aplikasi menggunakan artefak model dari Role 2 dan pengujian API berhasil, tetapi metrik Role 2 perlu dikoreksi dengan menghitung ulang exact-span TP/FP/FN dari test set yang sama. Jangan mengklaim seluruh tabel metrik sudah terverifikasi.

## Cara membuka demo Colab

1. Unduh `Role3_Article_NER_Service.zip` yang disediakan di chat.
2. Buka Notebook 05 — Run Role 3 App di repository kelompok.
3. Jalankan sel satu per satu dan unggah ZIP tersebut saat diminta.
4. Pastikan tes menunjukkan `9 passed`.
5. Klik tautan aplikasi yang dihasilkan oleh sel server.
6. Jangan memutus runtime Colab sebelum demo selesai; tautan web Colab bersifat sementara.
