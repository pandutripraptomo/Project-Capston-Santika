# app.py
import os
from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np
import re
# import ast # Tidak perlu jika Anda hanya memuat mlb.pickle

app = Flask(__name__)

# --- Muat Model ML yang Sudah Dilatih ---
try:
    # Memuat tokenizer
    with open('models/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    print("DEBUG: Tokenizer loaded successfully.")

    # Memuat MultiLabelBinarizer
    with open('models/mlb.pickle', 'rb') as handle:
        mlb = pickle.load(handle)
    print("DEBUG: MultiLabelBinarizer loaded successfully.")

    # Memuat max_sequence_length
    with open('models/max_sequence_length.txt', 'r') as f:
        MAX_SEQUENCE_LENGTH = int(f.read())
    print(f"DEBUG: Max sequence length loaded: {MAX_SEQUENCE_LENGTH}")

    # Memuat model TensorFlow/Keras
    model = tf.keras.models.load_model('models/chatbot_model.h5')
    print("DEBUG: TensorFlow model loaded successfully.")

except Exception as e:
    print(f"ERROR: Failed to load ML model components. Make sure 'models/' folder contains .h5, tokenizer.pickle, mlb.pickle, and max_sequence_length.txt. Details: {e}")
    # Jika model gagal dimuat, aplikasi tidak bisa berfungsi.
    # raise e # uncomment this line if you want the app to crash immediately on model init failure

# --- Fungsi Pra-pemrosesan Teks (Harus sama dengan yang digunakan saat pelatihan) ---
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# --- Fungsi Prediksi Jawaban ---
def predict_response(user_message):
    cleaned_message = clean_text(user_message)
    sequence = tokenizer.texts_to_sequences([cleaned_message])
    padded_sequence = pad_sequences(sequence, maxlen=MAX_SEQUENCE_LENGTH, padding='post', truncating='post')

    prediction = model.predict(padded_sequence)[0] # Ambil hasil prediksi untuk sampel tunggal
    
    # Ambil label yang probabilitasnya di atas ambang batas
    # Ambang batas ini bisa disesuaikan (misal 0.3, 0.5, 0.7)
    PREDICTION_THRESHOLD = 0.5 
    predicted_labels_indices = np.where(prediction > PREDICTION_THRESHOLD)[0]
    
    predicted_tags_list = []
    if len(predicted_labels_indices) > 0:
        # Gunakan mlb.inverse_transform untuk mendapatkan nama label
        # mlb.inverse_transform membutuhkan array biner, jadi kita buat array nol
        # dan set 1 di posisi yang diprediksi
        temp_binarized = np.zeros((1, len(mlb.classes_)))
        temp_binarized[0, predicted_labels_indices] = 1
        predicted_tags = mlb.inverse_transform(temp_binarized)[0]
        predicted_tags_list = list(predicted_tags)
    
    # --- LOGIKA UNTUK MENGHASILKAN JAWABAN BERDASARKAN LABEL YANG DIPREDIKSI ---
    # INI ADALAH BAGIAN YANG SANGAT PENTING DAN HARUS ANDA SESUAIKAN
    # DENGAN LABEL INDIVIDUAL YANG ADA DI mlb.classes_ ANDA DAN JAWABAN YANG RELEVAN.
    #
    # Contoh struktur responses dictionary:
    # Key adalah label individual (contoh: "fever", "headache")
    # Value adalah jawaban yang sesuai.
    # Jika ada banyak label, ini bisa menjadi dictionary yang sangat besar.
    # Anda perlu mengisi ini setelah mengetahui daftar final mlb.classes_ Anda dari Colab.

    # Catatan: Jawaban-jawaban ini sangat dasar dan hanya contoh.
    # Untuk kualitas, Anda perlu mengisi ini dengan konten kesehatan yang akurat.
    individual_responses = {
        "rash": "Ruam kulit bisa disebabkan oleh alergi atau iritasi. Hindari menggaruk dan jaga kebersihan area yang terkena.",
        "antibiotic": "Antibiotik harus digunakan sesuai resep dokter dan dihabiskan dosisnya, bahkan jika Anda merasa lebih baik.",
        "hepatitis b": "Hepatitis B adalah infeksi hati serius. Vaksinasi adalah cara terbaik untuk mencegahnya.",
        "celiac disease": "Penyakit Celiac adalah kondisi autoimun yang dipicu oleh gluten. Diet bebas gluten sangat penting.",
        "wart": "Kutil disebabkan oleh virus dan bisa menular. Pilihan pengobatan bervariasi, konsultasi dokter kulit dianjurkan.",
        "vitamin d": "Vitamin D penting untuk kesehatan tulang dan sistem kekebalan tubuh. Kekurangan Vitamin D umum terjadi.",
        "yeast infection": "Infeksi jamur sering terjadi dan bisa diobati dengan antijamur. Jaga kebersihan area intim.",
        "asthma": "Asma adalah kondisi saluran napas. Penting untuk membawa inhaler dan menghindari pemicu asma.",
        "ibuprofen": "Ibuprofen adalah obat anti-inflamasi non-steroid (OAINS) untuk meredakan nyeri dan demam.",
        "lung": "Kesehatan paru-paru vital untuk pernapasan. Hindari merokok dan paparan polutan.",
        "cough": "Batuk bisa jadi gejala banyak kondisi. Jika batuk berlanjut atau disertai gejala lain, konsultasi dokter.",
        "inhaler": "Inhaler adalah alat untuk mengantarkan obat langsung ke paru-paru, sering digunakan untuk asma atau PPOK.",
        "brain": "Kesehatan otak sangat penting. Lindungi kepala Anda dan jaga pola hidup sehat.",
        "lightheadedness": "Pusing ringan bisa disebabkan oleh dehidrasi atau tekanan darah rendah. Duduklah atau berbaring sebentar.",
        "dizziness": "Pusing bisa berarti banyak hal. Jika pusing parah atau disertai gejala lain, segera cari bantuan medis.",
        "coldness": "Perasaan dingin bisa dari suhu lingkungan atau kondisi medis. Pastikan Anda berpakaian hangat.",
        "allergic reaction": "Reaksi alergi bisa ringan hingga berat. Identifikasi alergen dan hindari kontak.",
        "genital herpes": "Herpes genital adalah infeksi menular seksual yang disebabkan oleh virus. Tidak ada obatnya, tapi gejalanya bisa dikelola.",
        "pregnancy": "Kehamilan adalah periode penting. Pastikan pemeriksaan rutin dan nutrisi yang cukup.",
        "unknown_topic": "Maaf, saya belum memiliki informasi spesifik mengenai topik ini. Bisakah Anda bertanya tentang gejala atau kondisi kesehatan umum?"
    }
    
    response_parts = []
    if not predicted_tags_list:
        response_text = individual_responses["unknown_topic"]
    else:
        for tag in predicted_tags_list:
            response_parts.append(individual_responses.get(tag, individual_responses["unknown_topic"]))
        
        # Gabungkan semua bagian respons. Anda bisa tambahkan kalimat pengantar
        if len(response_parts) > 1:
            response_text = "Berdasarkan pertanyaan Anda, saya bisa memberikan informasi tentang: " + " ".join(response_parts)
        else:
            response_text = response_parts[0]
            
        if not response_text: # Fallback jika entah kenapa kosong
            response_text = individual_responses["unknown_topic"]
            
    return response_text

# --- Rute Flask ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Panggil fungsi prediksi model ML Anda
        ai_response = predict_response(user_message)
        return jsonify({"response": ai_response})

    except Exception as e:
        print(f"Error during AI model prediction: {e}")
        return jsonify({"error": "Failed to get response from AI model. Please try again."}), 500

# --- Menjalankan Aplikasi Flask ---
if __name__ == '__main__':
    app.run(debug=True)