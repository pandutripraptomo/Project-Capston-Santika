# 💬 Health Chatbot Interaktif Berbasis Deep Learning 🩺


---

## ✨ Ringkasan Proyek

Ini adalah proyek Capstone yang ambisius: sebuah **Chatbot Kesehatan Interaktif** yang dirancang untuk memberikan informasi umum mengenai kesehatan dan medis dasar. Berbeda dengan banyak chatbot modern yang mengandalkan API model bahasa besar (LLM) eksternal, inti kecerdasan buatan dari chatbot ini sepenuhnya dibangun dan dilatih dari awal menggunakan **Deep Learning dengan TensorFlow**. Proyek ini menekankan pada pengembangan **aplikasi web Full-Stack** yang responsif dan menarik.

## 🚀 Fitur Utama

* **Antarmuka Pengguna (UI) yang Menarik & Responsif:** Desain modern dengan nuansa biru menenangkan, efek gradien, bayangan, dan animasi yang membuat pengalaman pengguna lebih menyenangkan di berbagai perangkat (desktop, tablet, mobile).
* **Kecerdasan Buatan Kustom:** Ditenagai oleh model Deep Learning (BiLSTM) yang dilatih secara mandiri untuk klasifikasi multi-label, mampu memprediksi kategori medis dari pertanyaan pengguna.
* **Backend Tangguh dengan Flask:** API RESTful yang efisien untuk mengelola komunikasi antara frontend dan model ML.
* **Pra-pemrosesan Data Canggih:** Implementasi teknik filtering label langka dan multi-label binarization untuk mengoptimalkan data pelatihan model.
* **Modular & Skalabel:** Struktur proyek yang jelas dan terorganisir, siap untuk pengembangan dan penambahan fitur di masa depan.

## 💡 Teknologi yang Digunakan

* **Frontend:** HTML5, CSS3 (Responsif), JavaScript (AJAX/Fetch API)
* **Backend:** Python 🐍, Flask
* **Machine Learning:** TensorFlow 2.x, Keras, scikit-learn (untuk preprocessing seperti MultiLabelBinarizer)
* **Manajemen Lingkungan:** `venv` (Virtual Environment), `pip`
* **Pengembangan & Pelatihan:** Visual Studio Code, Google Colab (untuk pelatihan model menggunakan GPU)

## 🏗️ Arsitektur Sistem

Sistem ini mengikuti arsitektur Client-Server, dengan komponen utama:

```mermaid
graph TD
    subgraph Alur Utama Chatbot (Permintaan & Respons)
        A_User((Pengguna)) -- Input Pertanyaan --> B_Frontend[Frontend: HTML/CSS/JS]

        B_Frontend -- Kirim Query (AJAX POST) --> C_BackendService[Backend: Flask]

        subgraph Komponen ML (Di dalam Backend)
            C_BackendService -- Proses Query --> D_Preprocess[Pra-pemrosesan Input]
            D_Preprocess -- Data Pra-proses --> E_Inference[Inferensi Model ML (BiLSTM)]
            E_Inference -- Hasil Prediksi --> F_PredictedTags[/Tag/Label Kesehatan Terprediksi/]
            F_PredictedTags -- Lookup/Generate Jawaban --> G_GenerateResponse[Generate Respons Teks]
        end

        G_GenerateResponse -- Respons Teks --> C_BackendService
        C_BackendService -- Kirim Respons (JSON) --> B_Frontend

        B_Frontend -- Tampilkan Respons --> A_User
    end

    subgraph Proses Muat Model (Saat Aplikasi Startup)
        H[Backend: Flask (Startup)] -- 1. Muat Model --> I[chatbot_model.h5]
        H -- 2. Muat Objek Pra-proses --> J[tokenizer.pickle & mlb.pickle & max_sequence_length.txt]
        I -- Model & Obj --> K[Backend: Flask (Siap Menerima Permintaan)]
        J -- Loaded --> K
    end

    H --> K
```
*Untuk melihat diagram alir ini dengan benar di GitHub, pastikan GitHub Anda mendukung rendering Mermaid atau gunakan ekstensi browser seperti "Mermaid Viewer".*

## ⚙️ Instalasi & Cara Menjalankan Proyek

Ikuti langkah-langkah di bawah ini untuk menjalankan chatbot ini di lingkungan lokal Anda.

### **Prasyarat**

* Python 3.8+ terinstal
* Git terinstal
* Akun Google (untuk Google Colab)

### **Langkah-langkah**

1.  **Kloning Repositori:**
    ```bash
    git clone [https://github.com/pandutripraptomo/Project-Capston-Santika.git](https://github.com/pandutripraptomo/Project-Capston-Santika.git)
    cd Project-Capston-Santika
    ```

2.  **Buat & Aktifkan Virtual Environment:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
    *Jika mengalami masalah aktivasi PowerShell, jalankan `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` sebagai Administrator.*

3.  **Instal Dependensi:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Jika `requirements.txt` belum ada, jalankan `pip install Flask pandas numpy tensorflow scikit-learn matplotlib jupyter ipykernel` lalu `pip freeze > requirements.txt`)*

4.  **Unduh & Letakkan Dataset:**
    * Unduh `train_data_chatbot.csv` dan `validation_data_chatbot.csv`.
    * Buat folder `data/` di direktori root proyek Anda.
    * Letakkan kedua file CSV di dalam folder `data/`.

5.  **Latih Model Machine Learning (Menggunakan Google Colab):**
    * Buka `notebooks/model_training.ipynb` di Google Colab.
    * Unggah `train_data_chatbot.csv` dan `validation_data_chatbot.csv` ke folder `/content/` di Colab.
    * Pastikan Anda mengubah path loading dataset di notebook Colab dari `../data/nama_file.csv` menjadi `nama_file.csv`.
    * Atur Runtime ke `GPU` (`Runtime > Change runtime type`).
    * Jalankan semua sel di notebook secara berurutan.
    * Setelah pelatihan selesai, **unduh semua file dari folder `models/` di Colab** (`chatbot_model.h5`, `tokenizer.pickle`, `mlb.pickle`, `max_sequence_length.txt`).
    * **Pindahkan file-file ini ke folder `models/` di direktori lokal proyek Anda.**

6.  **Jalankan Aplikasi Flask:**
    * Pastikan Anda berada di direktori root proyek dan `venv` aktif.
    * Jalankan perintah berikut:
        ```bash
        python app.py
        ```
    * Buka browser web Anda dan kunjungi: `http://127.0.0.1:5000/`

## 💬 Penggunaan Chatbot

Setelah aplikasi berjalan, buka browser dan ketikkan pertanyaan Anda di kolom input. Chatbot akan memproses pertanyaan Anda menggunakan model AI yang telah dilatih dan memberikan respons yang relevan.

## 🚧 Tantangan & Solusi

Proyek ini menghadirkan beberapa tantangan menarik:

* **Penyelesaian Masalah Lingkungan (venv & Kernel Crash):** Diatasi dengan pemahaman mendalam tentang manajemen virtual environment dan beralih ke Google Colab untuk pelatihan ML yang stabil.
* **Preprocessing Data Multi-Label Kompleks:** Mengatasi masalah `tags` yang berupa string list, filtering label langka (frekuensi rendah), dan memastikan keselarasan data input (X) dan label (Y) menggunakan `MultiLabelBinarizer` dan strategi filtering yang cermat.
* **Optimasi Model Deep Learning:** Dari model yang awalnya tidak belajar (0 parameter) hingga mencapai performa yang akurat dengan mengimplementasikan arsitektur **Bidirectional LSTM** yang kuat, `sigmoid` activation, dan `binary_crossentropy` loss.
* **Pembuatan Respons Dinamis:** Mengembangkan logika di backend untuk menerjemahkan prediksi multi-label menjadi jawaban yang informatif dari dictionary respons kustom.

## 🎯 Pengembangan Selanjutnya

* **Peningkatan Kualitas Jawaban:** Mengintegrasikan pencarian jawaban yang lebih dinamis dari dataset `short_answer` atau database.
* **Ekspansi Basis Pengetahuan:** Menambah data pelatihan untuk memperluas cakupan topik kesehatan.
* **Sesi Percakapan:** Mengimplementasikan penyimpanan riwayat percakapan untuk konteks.
* **Deployment:** Mendeploy aplikasi ke platform cloud (misal Heroku, Render) agar dapat diakses publik.

## ⚠️ Disclaimer

Chatbot ini adalah proyek Capstone yang dibuat untuk tujuan pembelajaran dan demonstrasi kemampuan teknis dalam Machine Learning dan Full-Stack Development. Informasi yang diberikan oleh chatbot ini bersifat umum dan **BUKAN PENGGANTI NASIHAT MEDIS PROFESIONAL**. Selalu konsultasikan dengan tenaga medis yang berkualifikasi untuk setiap masalah kesehatan.

## 🤝 Kontributor

- Pengembang Utama
- Pandu Tri Praptomo
- Aisyah Hanan
