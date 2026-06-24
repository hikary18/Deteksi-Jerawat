import streamlit as st
import os
import numpy as np
from PIL import Image

# ==========================================
# 1. OPTIMALISASI AWAL (Mencegah Lag & Flicker)
# ==========================================
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# ==========================================
# 2. KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="AcneCare AI - Premium Dermatological Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gaya CSS Premium & Estetik (Klinis, Bersih, Profesional)
st.markdown("""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #1E293B;
    }
    
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Header Banner Premium */
    .hero-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 40px 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-title {
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 8px;
        background: linear-gradient(90deg, #38BDF8, #34D399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 16px;
        color: #94A3B8;
        font-weight: 400;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p {
        color: #F1F5F9 !important;
    }
    
    /* Cards (Hasil Deteksi) */
    .result-card {
        background-color: white;
        border-radius: 16px;
        padding: 26px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 18px rgba(148, 163, 184, 0.08);
        margin-top: 15px;
        transition: transform 0.2s ease;
    }
    .result-card:hover {
        transform: translateY(-2px);
    }
    .result-header {
        font-size: 22px;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 15px;
        border-bottom: 2px solid #F1F5F9;
        padding-bottom: 10px;
        display: flex;
        align-items: center;
    }
    
    /* Badges untuk Tingkat Keparahan */
    .badge {
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-ringan { background-color: #D1FAE5; color: #065F46; border: 1px solid #A7F3D0; }
    .badge-sedang { background-color: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
    .badge-berat { background-color: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; }
    
    /* Chat UI Styling */
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 10px;
    }
    .chat-bubble {
        padding: 16px 20px;
        border-radius: 16px;
        margin-bottom: 16px;
        line-height: 1.6;
        font-size: 14.5px;
        box-shadow: 0 2px 8px rgba(148, 163, 184, 0.05);
    }
    .user-bubble {
        background-color: #E0F2FE;
        color: #0369A1;
        border-bottom-right-radius: 4px;
        margin-left: auto;
        max-width: 80%;
        border-left: 5px solid #0EA5E9;
    }
    .ai-bubble {
        background-color: white;
        color: #334155;
        border-bottom-left-radius: 4px;
        max-width: 80%;
        border-left: 5px solid #10B981;
        border: 1px solid #E2E8F0;
    }
    .sender-name {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
        display: block;
    }
    
    /* Customization for Streamlit Buttons */
    div.stButton > button {
        background-color: #0D9488 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 6px -1px rgba(13, 148, 136, 0.2) !important;
    }
    div.stButton > button:hover {
        background-color: #0F766E !important;
        box-shadow: 0 10px 15px -3px rgba(13, 148, 136, 0.3) !important;
        transform: translateY(-1px);
    }
    div.stButton > button:active {
        transform: translateY(1px);
    }
    
    /* Info Box */
    .info-box {
        background-color: #F0FDFA;
        border: 1px solid #CCFBF1;
        border-left: 5px solid #0D9488;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. KAMUS DATA DETAIL JERAWAT (BAHASA INDONESIA)
# ==========================================
ACNE_DETAILS = {
    "Blackheads": {
        "id_name": "Komedo Terbuka (Blackheads)",
        "severity": "Ringan (Mild)",
        "badge_class": "badge-ringan",
        "desc": "Komedo yang terbentuk akibat pori-pori tersumbat oleh sebum (minyak) dan sel kulit mati, di mana bagian atasnya terbuka dan teroksidasi oleh udara sehingga berwarna hitam.",
        "causes": "Produksi minyak berlebih, penumpukan sel kulit mati, dan perubahan hormon.",
        "solutions": "Gunakan pembersih wajah mengandung Salicylic Acid (BHA), hindari memencet komedo, dan lakukan eksfoliasi secara rutin (1-2 kali seminggu)."
    },
    "Cyst": {
        "id_name": "Jerawat Batu (Cystic Acne)",
        "severity": "Berat (Severe)",
        "badge_class": "badge-berat",
        "desc": "Jenis jerawat paling parah yang terbentuk jauh di dalam lapisan kulit, berupa benjolan besar, merah, keras, sakit saat disentuh, dan berisi nanah.",
        "causes": "Infeksi bakteri tersumbat jauh di dalam pori-pori, peradangan hebat, dan faktor genetik/hormonal.",
        "solutions": "JANGAN DIPENCET karena akan merusak struktur kulit dan menyebabkan bopeng (scars). Kompres dengan es batu dibalut handuk untuk mengurangi radang, gunakan basic skincare lembut, dan sangat direkomendasikan langsung ke Dokter Spesialis Kulit (Sp.DVE)."
    },
    "Papules": {
        "id_name": "Papula (Benjolan Merah tanpa Nanah)",
        "severity": "Sedang (Moderate)",
        "badge_class": "badge-sedang",
        "desc": "Benjolan kecil berwarna kemerahan di permukaan kulit yang terasa nyeri saat disentuh. Belum memiliki titik putih nanah di puncaknya.",
        "causes": "Penyumbatan pori-pori yang memicu peradangan dinding folikel rambut akibat bakteri P. acnes.",
        "solutions": "Gunakan obat totol jerawat yang mengandung Benzoyl Peroxide atau Centella Asiatica untuk menenangkan kulit. Hindari scrub wajah fisik selama meradang."
    },
    "Pustules": {
        "id_name": "Pustula (Benjolan Merah Berlesi Nanah)",
        "severity": "Sedang (Moderate)",
        "badge_class": "badge-sedang",
        "desc": "Jerawat meradang yang memiliki puncak berwarna putih atau kekuningan di tengahnya karena berisi nanah.",
        "causes": "Infeksi bakteri lanjutan pada pori-pori tersumbat yang menyebabkan sel darah putih berkumpul di area radang.",
        "solutions": "Gunakan obat totol jerawat mengandung Benzoyl Peroxide atau Sulfur. Hindari memencetnya agar infeksi bakteri tidak menyebar ke area kulit lain."
    },
    "Whiteheads": {
        "id_name": "Komedo Tertutup (Whiteheads)",
        "severity": "Ringan (Mild)",
        "badge_class": "badge-ringan",
        "desc": "Komedo yang terbentuk karena pori-pori tersumbat sepenuhnya oleh minyak dan sel kulit mati, tertutup oleh lapisan kulit tipis sehingga tampak seperti bintil putih.",
        "causes": "Sumbatan minyak pada pori-pori yang tidak terekspos udara bebas.",
        "solutions": "Gunakan skincare non-comedogenic, pembersih wajah berbahan lembut, dan retinol atau AHA/BHA untuk merangsang regenerasi kulit."
    }
}

# ==========================================
# 4. DATABASE TANYA JAWAB CHATBOT (BISA DIISI/DIEDIT SENDIRI)
# ==========================================
CHATBOT_DATABASE = {
    "✨ Rekomendasi Skincare Dasar": {
        "Bagaimana urutan basic skincare yang benar untuk kulit berjerawat?": 
            "Urutan basic skincare yang aman untuk kulit berjerawat adalah:\n\n"
            "1. **Double Cleansing**: Bersihkan wajah menggunakan micellar water lalu cuci muka dengan sabun lembut.\n"
            "2. **Moisturizer**: Gunakan pelembap bertekstur gel ringan yang berlabel *non-comedogenic*.\n"
            "3. **Sunscreen**: Gunakan tabir surya SPF 30 atau lebih di siang hari untuk mencegah noda jerawat menjadi hitam.",
        "Kandungan skincare apa saja yang ampuh mengatasi jerawat?": 
            "Beberapa kandungan aktif yang sangat direkomendasikan untuk kulit berjerawat antara lain:\n\n"
            "- **Salicylic Acid (BHA)**: Membersihkan minyak berlebih jauh ke dalam pori-pori.\n"
            "- **Niacinamide / Centella Asiatica**: Menenangkan kulit yang meradang dan merah.\n"
            "- **Tea Tree Oil**: Memiliki sifat antibakteri alami untuk melawan bakteri penyebab jerawat."
    },
    "⚠️ Kebiasaan & Penyebab Jerawat": {
        "Mengapa jerawat saya tidak kunjung sembuh?": 
            "Jerawat yang membandel atau sulit sembuh bisa dipicu oleh beberapa hal:\n\n"
            "- Sering menyentuh atau memencet jerawat dengan tangan kotor.\n"
            "- Jarang membersihkan sarung bantal atau layar handphone.\n"
            "- Stres berlebih, kurang tidur, atau ketidakseimbangan hormon.\n"
            "- Terlalu sering bergonta-ganti produk skincare baru dalam waktu singkat.",
        "Apakah pola makan manis dan susu bisa memicu jerawat?": 
            "Ya, benar. Makanan tinggi gula (*high glycemic*) serta produk olahan susu (*dairy products*) dapat merangsang hormon insulin. Lonjakan insulin ini memicu produksi kelenjar minyak secara berlebihan, yang akhirnya menyumbat pori-pori wajah Anda."
    },
    "🩹 Solusi Penanganan Mandiri": {
        "Apa yang harus dilakukan saat jerawat batu terasa sakit?": 
            "Jika Anda memiliki jerawat batu (Cystic Acne) yang sakit dan bengkak:\n\n"
            "1. **Kompres Es Batu**: Bungkus es batu dengan handuk bersih, kompres pada jerawat selama 5 menit untuk meredakan nyeri dan bengkak.\n"
            "2. **Gunakan Obat Totol**: Aplikasikan obat totol dengan kandungan Sulfur atau Benzoyl Peroxide.\n"
            "3. **Hindari Scrub**: Jangan gunakan scrub wajah fisik karena akan merusak barier kulit Anda.\n"
            "4. **Jangan Dipencet**: Memencet jerawat batu akan merusak jaringan kulit dalam dan memicu bopeng (*scars*).",
        "Bagaimana cara menghilangkan bekas jerawat kemerahan (PIE)?": 
            "Untuk meredakan bekas jerawat kemerahan (PIE), gunakan skincare yang fokus pada pemulihan *skin barrier* dan anti-inflamasi, seperti produk yang mengandung **Centella Asiatica**, **Niacinamide**, **Ceramide**, atau **Snail Mucin**. Jangan lupa untuk selalu disiplin menggunakan sunscreen setiap hari agar kondisinya tidak memburuk."
    }
}

# ==========================================
# 5. CACHING SEBAGAI LAZY LOADING
# ==========================================
@st.cache_resource
def load_acne_model():
    import tensorflow as tf
    model_path = "model_jerawat_5kelas.keras"
    if os.path.exists(model_path):
        return tf.keras.models.load_model(model_path)
    return None

@st.cache_resource
def get_class_names():
    if os.path.exists("class_names.txt"):
        with open("class_names.txt", "r") as f:
            return [line.strip() for line in f.readlines()]
    return ["Blackheads", "Cyst", "Papules", "Pustules", "Whiteheads"]

class_names = get_class_names()

# ==========================================
# 6. INITIALIZE SESSION STATE (Anti-Flicker)
# ==========================================
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "image_source" not in st.session_state:
    st.session_state.image_source = None
if "prediction_done" not in st.session_state:
    st.session_state.prediction_done = False
if "predicted_class" not in st.session_state:
    st.session_state.predicted_class = None
if "confidence" not in st.session_state:
    st.session_state.confidence = 0.0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "model", "text": "Halo! Saya adalah **AcneCare AI Guide**. Saya siap membantu Anda memberikan informasi terpercaya seputar kesehatan kulit wajah dan jerawat tanpa perlu koneksi API Key.\n\nSilakan pilih salah satu kategori keluhan di panel sebelah kanan untuk menampilkan pertanyaan terarah!"}
    ]

# ==========================================
# 7. SIDEBAR & MENU NAVIGASI
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2854/2854101.png", width=90)
st.sidebar.title("AcneCare AI")
st.sidebar.caption("Sistem Diagnosis & Konsultasi Jerawat")
menu = st.sidebar.radio("PILIH LAYANAN UTAMA:", ["🔎 Deteksi Jerawat AI", "💬 Tanya Jawab Chatbot"])

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);'>
    <h4 style='margin-top:0; color:#38BDF8;'>🔒 Sistem Aman & Lokal</h4>
    <p style='font-size: 11.5px; color:#94A3B8; margin-bottom: 0;'>Proses deteksi dan visualisasi berjalan sepenuhnya di komputer Anda secara luring (offline) tanpa mengirimkan data wajah ke server luar.</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# MENU 1: DETEKSI JERAWAT AI
# ==========================================
if menu == "🔎 Deteksi Jerawat AI":
    # Hero Header Banner
    st.markdown("""
        <div class='hero-banner'>
            <div class='hero-title'>🩺 AcneCare AI Detection System</div>
            <div class='hero-subtitle'>Analisis tingkat keparahan, penyebab, dan solusi penanganan jerawat secara presisi menggunakan Deep Learning</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("📸 Masukan Gambar Kulit")
        src_option = st.radio("Metode Input:", ["Unggah File Gambar", "Gunakan Kamera Wajah"], horizontal=True)
        
        temp_img = None
        if src_option == "Unggah File Gambar":
            temp_img = st.file_uploader("Pilih gambar wajah (JPG, JPEG, PNG)...", type=["jpg", "jpeg", "png"])
        else:
            temp_img = st.camera_input("Ambil foto wajah secara langsung")
            
        if temp_img is not None:
            is_new_image = False
            if st.session_state.uploaded_image is None:
                is_new_image = True
            else:
                name_current = getattr(st.session_state.uploaded_image, 'name', None)
                name_new = getattr(temp_img, 'name', None)
                if name_current != name_new:
                    is_new_image = True
                    
            if is_new_image:
                st.session_state.uploaded_image = temp_img
                st.session_state.image_source = src_option
                st.session_state.prediction_done = False
                st.session_state.predicted_class = None
                st.session_state.confidence = 0.0
            
    with col2:
        st.subheader("📊 Laporan Diagnosis Medis")
        
        if st.session_state.uploaded_image is not None:
            try:
                image = Image.open(st.session_state.uploaded_image)
                st.image(image, caption="Gambar Input", use_column_width=True)
                st.write("")
                
                if st.button("Mulai Analisis Deteksi", use_container_width=True):
                    with st.spinner("Sistem sedang mencocokkan matriks piksel..."):
                        model = load_acne_model()
                        
                        if model is None:
                            st.error("Gagal memuat model. File 'model_jerawat_5kelas.keras' tidak ditemukan.")
                        else:
                            # Preprocessing
                            img_resized = image.resize((224, 224))
                            img_array = np.array(img_resized)
                            
                            if img_array.shape[-1] == 4:
                                img_array = img_array[..., :3]
                            
                            img_array = img_array / 255.0
                            img_array = np.expand_dims(img_array, axis=0)
                            
                            prediction = model.predict(img_array)
                            class_idx = np.argmax(prediction)
                            
                            # Simpan ke state agar permanen dan stabil di layar
                            st.session_state.predicted_class = class_names[class_idx]
                            st.session_state.confidence = np.max(prediction) * 100
                            st.session_state.prediction_done = True
                            st.rerun()
                
                if st.session_state.prediction_done and st.session_state.predicted_class is not None:
                    predicted_class = st.session_state.predicted_class
                    confidence = st.session_state.confidence
                    
                    details = ACNE_DETAILS.get(predicted_class, {
                        "id_name": predicted_class,
                        "severity": "Tidak diketahui",
                        "badge_class": "badge-ringan",
                        "desc": "Kondisi tidak terdefinisi.",
                        "causes": "Tidak diketahui.",
                        "solutions": "Silakan hubungi dokter spesialis kulit."
                    })
                    
                    st.markdown(f"""
                        <div class='result-card'>
                            <div class='result-header'>
                                🩺 Hasil Analisis Dermatologi
                            </div>
                            <span class='badge {details['badge_class']}'>{details['severity']}</span>
                            <h3 style='margin-top: 5px; color: #0F172A; font-weight:700;'>{details['id_name']}</h3>
                            <div style='margin: 15px 0; background-color:#F8FAFC; padding: 12px; border-radius:8px; border: 1px solid #E2E8F0;'>
                                <b style='color:#0D9488;'>Akurasi Keyakinan Model:</b> {confidence:.2f}%
                            </div>
                            <p><b>Deskripsi Kondisi:</b><br>{details['desc']}</p>
                            <p><b>Penyebab Utama:</b><br>{details['causes']}</p>
                            <p><b>Saran Solusi Terarah:</b><br>{details['solutions']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if predicted_class == "Cyst":
                        st.warning("🚨 **Rujukan Medis:** Jerawat Batu (Cystic) tergolong jerawat berat dengan risiko bopeng permanen yang tinggi. Hindari menekan area ini sendiri dan segera konsultasikan dengan Dokter Spesialis Kulit (Sp.DVE).")
                    else:
                        st.success("👍 Diagnosis selesai. Silakan terapkan rekomendasi perawatan mandiri ringan secara konsisten.")
                                
            except Exception as e:
                st.error(f"Gagal memproses gambar: {str(e)}")
        else:
            st.info("Silakan unggah gambar wajah atau gunakan kamera depan pada panel kiri untuk mendapatkan visualisasi hasil analisis medis di sini.")

# ==========================================
# MENU 2: TANYA JAWAB CHATBOT AI
# ==========================================
elif menu == "💬 Tanya Jawab Chatbot":
    # Hero Header Banner Chatbot
    st.markdown("""
        <div class='hero-banner' style='background: linear-gradient(135deg, #0D9488 0%, #0F766E 100%);'>
            <div class='hero-title' style='background:none; -webkit-text-fill-color:white; color:white;'>💬 AcneCare Q&A Guide</div>
            <div class='hero-subtitle' style='color:#CCFBF1;'>Sistem Konsultasi Interaktif Offline — Temukan solusi terpercaya seputar kesehatan kulit tanpa internet</div>
        </div>
    """, unsafe_allow_html=True)

    chat_col, guide_col = st.columns([1.2, 0.8], gap="large")

    with chat_col:
        st.subheader("💬 Alur Konsultasi")
        
        # Gelembung Chat yang Estetik
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown(f"""
                    <div class='chat-bubble user-bubble'>
                        <span class='sender-name' style='color:#0284C7;'>Anda</span>
                        {chat['text']}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class='chat-bubble ai-bubble'>
                        <span class='sender-name' style='color:#059669;'>AcneCare AI</span>
                        {chat['text']}
                    </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with guide_col:
        st.subheader("❓ Pustaka Pertanyaan")
        st.markdown("""
        <div class='info-box'>
            <b>Cara Konsultasi:</b><br>
            Silakan pilih salah satu kategori di bawah ini, lalu klik tombol pertanyaan untuk langsung mendapatkan jawaban dari asisten AI.
        </div>
        """, unsafe_allow_html=True)
        
        # Iterasi Kategori Database yang Lebih Cantik
        for category, qa_pairs in CHATBOT_DATABASE.items():
            with st.expander(category, expanded=True):
                for question, answer in qa_pairs.items():
                    # Tombol Pertanyaan yang dipersonalisasi
                    if st.button(question, key=question, use_container_width=True):
                        st.session_state.chat_history.append({"role": "user", "text": question})
                        st.session_state.chat_history.append({"role": "model", "text": answer})
                        st.rerun()
                        
        st.write("")
        if st.button("🧹 Reset Obrolan", use_container_width=True):
            st.session_state.chat_history = [
                {"role": "model", "text": "Halo! Saya adalah **AcneCare AI Guide**. Silakan pilih salah satu pertanyaan yang sudah disediakan di atas untuk mulai berdiskusi!"}
            ]
            st.rerun()