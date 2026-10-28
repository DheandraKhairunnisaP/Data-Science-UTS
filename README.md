# Article NER Service

Proyek ini dibuat untuk tugas UTS NLP. Aplikasi menerima judul dan isi artikel berita, kemudian menampilkan entitas bernama yang ditemukan oleh model, jenis entitasnya, dan posisi karakter di dalam teks.

## Apa itu NER?

Named-Entity Recognition (NER) adalah proses mengenali nama atau informasi tertentu dalam teks, lalu memberi label pada bagian tersebut. Pada proyek ini, NER digunakan untuk mencari entitas seperti orang, organisasi, lokasi, tanggal, dan peristiwa.

Aplikasi memakai pipeline spaCy `ner_custom_v1` dari tahap Role 2. Hasil prediksi bisa saja melewatkan nama atau memberikan label yang keliru, sehingga hasil tetap perlu diperiksa.

## Cara kerja aplikasi

1. Pengguna mengisi judul dan isi artikel di halaman web.
2. Frontend mengirimkan data ke endpoint `POST /extract-entities`.
3. Backend FastAPI menggabungkan judul dan isi artikel, lalu memprosesnya dengan model NER.
4. Hasil ditampilkan sebagai tabel berisi teks entitas, label, posisi awal, dan posisi akhir; teks artikel juga diberi sorotan.

Label yang ditampilkan adalah `PERSON`, `ORG`, `GPE`, `LOC`, `DATE`, dan `EVENT`, jika dikenali oleh model.

## Menjalankan di Google Colab

Buka [Notebook Role 3 — Jalankan Aplikasi](https://colab.research.google.com/drive/1ha284rNZHtT1ObXsZTlahDYOh0sSsXw1#scrollTo=0a183d2d), lalu jalankan sel dari atas ke bawah. Notebook mengambil source code dan model dari repository, memasang dependensi, menjalankan tes API, dan membuka tautan sementara untuk halaman web.


## Menjalankan di komputer sendiri

Gunakan Python yang kompatibel dengan spaCy 3.8.

1. Pasang dependensi dari folder utama repository:

   ```bash
   pip install -r requirements.txt
   ```

2. Ekstrak model dari `models/ner_custom_v1.zip` ke folder `models/ner_custom_v1/`. Setelah diekstrak, file `config.cfg` harus berada langsung di dalam folder tersebut.

   PowerShell:
   ```powershell
   Expand-Archive -LiteralPath models/ner_custom_v1.zip -DestinationPath models/ner_custom_v1 -Force
   ```

   Linux/macOS:
   ```bash
   python -m zipfile -e models/ner_custom_v1.zip models/ner_custom_v1
   ```

3. Jalankan server:

   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

4. Buka `http://127.0.0.1:8000`. Dokumentasi API tersedia di `http://127.0.0.1:8000/docs`.

5. Jalankan pengujian:

   ```bash
   python -m pytest -q
   ```

## Endpoint API

Endpoint utama adalah `POST /extract-entities`.

Contoh request:

```json
{
  "title": "Judul artikel",
  "body": "Isi artikel berita."
}
```

Response berisi array `entities` serta metadata pada `meta`. Setiap entitas memiliki `text`, `label`, `start`, dan `end`.

Posisi karakter dihitung dari awal teks gabungan `title + newline + body`. Indeks dimulai dari nol, `start` termasuk karakter pertama, sedangkan `end` tidak termasuk karakter setelah teks entitas.

## Pembagian pekerjaan

- ** Alvina Nur Laila A (Role 1) Data dan anotasi:** memeriksa dataset, membersihkan data, menyiapkan anotasi entitas, dan memeriksa konsistensi label.
- ** Nadia Tifara S (Role 2) Model dan evaluasi:** melatih atau mengadaptasi model NER dan mengevaluasi hasilnya.
- ** Dheandra Khairunnisa P (Role 3) Aplikasi:** membuat API, halaman web, validasi input, dan pengujian integrasi.

## Berkas dalam repository

- `models/Data_&_Anotasi.ipynb`: notebook pekerjaan data dan anotasi.
- `models/Training_Model_NER_UTS (1).ipynb`: notebook training model.
- `models/ner_custom_v1.zip`: artefak model yang digunakan aplikasi.
- `notebooks/01_profiling_dataset.ipynb`, `02_prepare_annotation.ipynb`, dan `03_train_evaluate_ner.ipynb`: notebook alur kerja data dan model.
- `app/main.py`: backend API.
- `web/index.html`: antarmuka web.
- `tests/test_api.py`: pengujian API.
- `docs/`: contoh request dan catatan evaluasi.

CSV dataset mentah yang diberikan dosen tidak disertakan dalam repository.

## Documentation Video
- (https://drive.google.com/drive/folders/1QYFRxhkaTELBSp5HBqtMt07KvI7DnRZ4?usp=drive_link) Dokumentasi berupa video demo untuk melihat hasil dashboard.
