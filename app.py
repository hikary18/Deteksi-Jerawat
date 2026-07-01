import streamlit as st
import os
import numpy as np
from PIL import Image
from datetime import datetime

# ==========================================
# 1. OPTIMALISASI AWAL (Mencegah Lag & Flicker)
# ==========================================
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# ==========================================
# 2. KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="AcneCare AI - Premium Medicio Style Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Menggunakan aksen utama teal (#3fbbc0) dan abu-abu klinis lembut (#f1f6fe)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Reset Global & Background */
    html, body, [data-testid="stSidebar"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #F8FAFC !important;
    }
    
    /* 1. TOP UTILITY BAR (Teal Header) */
    .medicio-top-bar {
        background-color: #3fbbc0;
        color: #FFFFFF;
        padding: 10px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 0px;
        border-radius: 0px;
    }
    .top-bar-left {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .top-bar-right {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    /* 2. BRAND BAR (Navigation Area) */
    .medicio-brand-bar {
        background-color: #FFFFFF;
        padding: 15px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
    }
    .brand-logo-container {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .brand-emblem {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background: linear-gradient(45deg, #FF6B6B, #4D96FF, #6BCB77, #FFD93D);
        display: inline-block;
    }
    .brand-title {
        font-size: 24px;
        font-weight: 800;
        color: #2c4964;
        letter-spacing: -0.5px;
    }
    .brand-title span {
        color: #3fbbc0;
    }
    .brand-nav {
        display: flex;
        gap: 20px;
        font-size: 13px;
        font-weight: 600;
        color: #2c4964;
    }
    .brand-nav-item {
        color: #2c4964;
        text-decoration: none;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .brand-nav-item.active {
        color: #3fbbc0;
    }
    .brand-btn {
        background-color: #3fbbc0;
        color: white;
        padding: 8px 18px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        border: none;
    }

    /* 3. HERO SLIDER BANNER (image_a953c4.jpg style) */
    .medicio-hero-section {
        background: linear-gradient(135deg, rgba(63,187,192,0.1) 0%, rgba(241,246,254,0.9) 100%), 
                    url('https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&q=80&w=1200');
        background-size: cover;
        background-position: center;
        border-radius: 16px;
        height: 380px;
        position: relative;
        margin-bottom: 35px;
        box-shadow: inset 0 0 100px rgba(0,0,0,0.05);
        display: flex;
        align-items: flex-end;
        justify-content: center;
        padding-bottom: 30px;
    }
    .medicio-hero-card {
        background-color: rgba(255, 255, 255, 0.95);
        border-top: 4px solid #3fbbc0;
        padding: 30px 40px;
        width: 85%;
        border-radius: 8px;
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
        text-align: center;
    }
    .medicio-hero-card h1 {
        font-size: 32px;
        font-weight: 800;
        color: #2c4964 !important;
        margin-top: 0;
        margin-bottom: 12px;
        letter-spacing: -0.5px;
    }
    .medicio-hero-card p {
        font-size: 14px;
        color: #64748B;
        max-width: 800px;
        margin: 0 auto 15px auto;
        line-height: 1.6;
    }
    .medicio-hero-btn {
        background-color: #3fbbc0;
        color: white;
        padding: 10px 24px;
        border-radius: 4px;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        display: inline-block;
        box-shadow: 0 4px 6px rgba(63, 187, 192, 0.2);
    }

    /* 4. 4-COLUMN FEATURE CARDS GRID */
    .medicio-feature-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-bottom: 35px;
    }
    .medicio-feature-card {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 8px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
        border-bottom: 3px solid transparent;
        transition: transform 0.2s, border-color 0.2s;
    }
    .medicio-feature-card:hover {
        transform: translateY(-5px);
        border-color: #3fbbc0;
    }
    .medicio-feature-card-icon {
        color: #3fbbc0;
        font-size: 28px;
        margin-bottom: 15px;
    }
    .medicio-feature-card h4 {
        color: #2c4964 !important;
        font-size: 16px;
        font-weight: 700;
        margin-top: 0;
        margin-bottom: 10px;
    }
    .medicio-feature-card p {
        color: #64748B;
        font-size: 12.5px;
        line-height: 1.6;
        margin-bottom: 0;
    }

    /* KARTU HASIL DIAGNOSIS PREMIUM (MEDICIO THEME) */
    .medicio-result-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 24px;
        border-left: 6px solid #3fbbc0;
        box-shadow: 0 8px 24px rgba(0,0,0,0.05);
        margin-top: 15px;
    }
    .medicio-result-card h3 {
        color: #2c4964 !important;
        font-size: 22px;
        font-weight: 800;
        margin-top: 0;
        margin-bottom: 15px;
    }

    /* BADGES & LABELS */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-ringan { background-color: #E6F7F8; color: #1f8e94; }
    .badge-sedang { background-color: #FEF3C7; color: #B45309; }
    .badge-berat { background-color: #FEE2E2; color: #B91C1C; }

    /* CHAT BUBBLES INTERAKTIF */
    .chat-bubble { 
        padding: 14px 18px; 
        border-radius: 8px; 
        margin-bottom: 15px; 
        max-width: 85%; 
        line-height: 1.6;
        font-size: 13.5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    .user-bubble { 
        background-color: #E6F7F8; 
        color: #2c4964; 
        border-bottom-right-radius: 0px;
        margin-left: auto;
        border-right: 4px solid #3fbbc0;
    }
    .ai-bubble { 
        background-color: #FFFFFF; 
        color: #475569; 
        border-bottom-left-radius: 0px;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #2c4964;
    }

    /* KOTAK RUTINITAS */
    .routine-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        margin-top: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }
    .routine-header {
        font-size: 16px;
        font-weight: 700;
        color: #2c4964;
        margin-bottom: 15px;
        border-bottom: 2px solid #F1F5F9;
        padding-bottom: 10px;
    }

    /* CUSTOM TOMBOL STREAMLIT (MEDICIO STYLE) */
    .stButton>button {
        background: #3fbbc0 !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 4px !important;
        border: none !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 10px rgba(63, 187, 192, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background: #319fa3 !important;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. KAMUS DATA DETAIL JERAWAT & RUTINITAS
# ==========================================
ACNE_DETAILS = {
    "Blackheads": {
        "id_name": "Komedo Terbuka (Blackheads)",
        "severity": "Ringan (Mild)",
        "badge_class": "badge-ringan",
        "desc": "Komedo yang terbentuk akibat pori-pori tersumbat oleh sebum (minyak) dan sel kulit mati, di mana bagian atasnya terbuka dan teroksidasi oleh udara sehingga berwarna hitam.",
        "causes": "Produksi minyak berlebih, penumpukan sel kulit mati, dan perubahan hormon.",
        "solutions": "Gunakan pembersih wajah mengandung Salicylic Acid (BHA), hindari memencet komedo, dan lakukan eksfoliasi secara rutin (1-2 kali seminggu).",
        "routine_am": [
            "Gunakan pembersih wajah berbahan lembut (Gentle Cleanser)",
            "Gunakan Hydrating Toner untuk mengembalikan pH kulit",
            "Gunakan serum Niacinamide (mengontrol produksi sebum)",
            "Gunakan pelembap bertekstur gel ringan (Non-comedogenic Moisturizer)",
            "Wajib gunakan Sunscreen minimal SPF 30 (Physical Sunscreen disarankan)"
        ],
        "routine_pm": [
            "Lakukan Double Cleansing (Micellar Water / Cleansing Balm diikuti Gentle Cleanser)",
            "Gunakan obat eksfoliasi kimiawi mengandung Salicylic Acid (BHA) - 2 kali seminggu",
            "Gunakan pelembap (Moisturizer) untuk mengunci kelembapan semalaman"
        ]
    },
    "Cyst": {
        "id_name": "Jerawat Batu (Cystic Acne)",
        "severity": "Berat (Severe)",
        "badge_class": "badge-berat",
        "desc": "Jenis jerawat paling parah yang terbentuk jauh di dalam lapisan kulit, berupa benjolan besar, merah, keras, sakit saat disentuh, dan berisi nanah.",
        "causes": "Infeksi bakteri tersumbat jauh di dalam pori-pori, peradangan hebat, dan faktor genetik/hormonal.",
        "solutions": "JANGAN DIPENCET karena akan merusak struktur kulit dan menyebabkan bopeng (scars). Kompres dengan es batu dibalut handuk untuk mengurangi radang, gunakan basic skincare lembut, dan sangat direkomendasikan langsung ke Dokter Spesialis Kulit (Sp.DVE).",
        "routine_am": [
            "Pembersih wajah dengan formula khusus kulit sensitif / bebas sabun (Soap-free Cleanser)",
            "Gunakan Hydrating Toner penenang (mengandung Centella Asiatica atau Panthenol)",
            "Gunakan Moisturizer Barrier untuk memperbaiki struktur kulit luar yang rusak",
            "Gunakan Physical Sunscreen SPF 30/50 tanpa parfum"
        ],
        "routine_pm": [
            "Pembersih wajah ultra-lembut (tanpa scrub)",
            "Kompres area radang dengan es batu yang dibungkus kain steril selama 5 menit",
            "Gunakan Acne Patch pada bagian jerawat yang berpotensi pecah",
            "Gunakan pelembap tebal (Moisturizer) untuk memulihkan kelembapan alami"
        ]
    },
    "Papules": {
        "id_name": "Papula (Benjolan Merah tanpa Nanah)",
        "severity": "Sedang (Moderate)",
        "badge_class": "badge-sedang",
        "desc": "Benjolan kecil berwarna kemerahan di permukaan kulit yang terasa nyeri saat disentuh. Belum memiliki titik putih nanah di puncaknya.",
        "causes": "Penyumbatan pori-pori yang memicu peradangan dinding folikel rambut akibat bakteri P. acnes.",
        "solutions": "Gunakan obat totol jerawat yang mengandung Benzoyl Peroxide atau Centella Asiatica untuk menenangkan kulit. Hindari scrub wajah fisik selama meradang.",
        "routine_am": [
            "Gunakan pembersih wajah berbusa lembut (Gentle Cleanser)",
            "Gunakan Toner penenang kulit kemerahan (Soothing Toner)",
            "Gunakan Moisturizer bertekstur air/gel ringan",
            "Wajib gunakan Sunscreen SPF 30 (bebas minyak)"
        ],
        "routine_pm": [
            "Lakukan Double Cleansing dengan micellar water berbasis air",
            "Gunakan obat totol jerawat (Spot Treatment) mengandung Benzoyl Peroxide / Salicylic Acid pada bagian papula",
            "Gunakan Soothing Serum (Cica / Tea Tree)",
            "Gunakan Moisturizer ringan"
        ]
    },
    "Pustules": {
        "id_name": "Pustula (Benjolan Merah Berlesi Nanah)",
        "severity": "Sedang (Moderate)",
        "badge_class": "badge-sedang",
        "desc": "Jerawat meradang yang memiliki puncak berwarna putih atau kekuningan di tengahnya karena berisi nanah.",
        "causes": "Infeksi bakteri lanjutan pada pori-pori tersumbat yang menyebabkan sel darah putih berkumpul di area radang.",
        "solutions": "Gunakan obat totol jerawat mengandung Benzoyl Peroxide atau Sulfur. Hindari memencetnya agar infeksi bakteri tidak menyebar ke area kulit lain.",
        "routine_am": [
            "Pembersih wajah lembut anti-bakteri",
            "Gunakan Toner penenang (mengandung Green Tea atau Centella)",
            "Gunakan Pelembap gel bebas minyak",
            "Gunakan Sunscreen dengan klaim Acne-safe"
        ],
        "routine_pm": [
            "Lakukan Double Cleansing secara perlahan (jangan digosok kencang)",
            "Gunakan obat totol jerawat khusus yang mengandung Sulfur / Salicylic Acid untuk mengeringkan nanah secara steril",
            "Gunakan Moisturizer barrier untuk mencegah iritasi kulit sekitar"
        ]
    },
    "Whiteheads": {
        "id_name": "Komedo Tertutup (Whiteheads)",
        "severity": "Ringan (Mild)",
        "badge_class": "badge-ringan",
        "desc": "Komedo yang terbentuk karena pori-pori tersumbat sepenuhnya oleh minyak dan sel kulit mati, tertutup oleh lapisan kulit tipis sehingga tampak seperti bintil putih.",
        "causes": "Sumbatan minyak pada pori-pori yang tidak terekspos udara bebas.",
        "solutions": "Gunakan skincare non-comedogenic, pembersih wajah berbahan lembut, dan retinol atau AHA/BHA untuk merangsang regenerasi kulit.",
        "routine_am": [
            "Gunakan pembersih wajah yang mengandung asam salisilat dosis rendah",
            "Gunakan Hydrating Toner",
            "Gunakan Moisturizer bertekstur gel cair yang mudah menyerap",
            "Gunakan Sunscreen non-comedogenic"
        ],
        "routine_pm": [
            "Lakukan Double Cleansing untuk membersihkan pori secara tuntas",
            "Gunakan bahan aktif eksfoliasi AHA (Glycolic Acid / Lactic Acid) - 2 kali seminggu untuk mengangkat sel kulit mati di permukaan",
            "Gunakan Moisturizer untuk melembapkan kulit"
        ]
    }
}

# ==========================================
# 4. DATABASE CHATBOT OFFLINE (LOKAL)
# ==========================================
CHATBOT_DATABASE = {
    "skincare": "Urutan basic skincare yang wajib dilakukan untuk kulit berjerawat adalah: \n1. **Cleanser** (pilihlah sabun muka yang lembut tanpa scrub).\n2. **Moisturizer** (pelembap bertekstur gel ringan non-comedogenic).\n3. **Sunscreen** (tabir surya fisik dengan SPF minimal 30 di pagi/siang hari untuk mencegah bopeng kehitaman).",
    "pencet": "Jerawat **SANGAT TIDAK BOLEH** dipencet secara paksa. Memencet jerawat dapat merusak dinding folikel kulit, mendorong kotoran dan bakteri masuk lebih dalam ke lapisan dermis, serta memicu bopeng (*ice pick scars*) permanen yang sulit disembuhkan.",
    "batu": "Jerawat Batu (Cystic Acne) tergolong jerawat dengan tingkat keparahan **BERAT**. Jerawat ini dipicu oleh bakteri yang menyumbat folikel sangat dalam. Penanganan terbaik adalah dengan mengompres dingin menggunakan es batu dibungkus handuk steril untuk meredakan nyeri dan segera mengonsultasikan ke dokter spesialis kulit untuk diresepkan antibiotik minum.",
    "makanan": "Beberapa jenis makanan dapat memicu peningkatan produksi sebum yang memperparah jerawat, di antaranya:\n1. Makanan tinggi indeks glikemik (manis, tepung, nasi putih berlebih).\n2. Produk olahan susu sapi (*dairy products* seperti susu murni dan keju).\n3. Makanan berminyak dan tinggi lemak jenuh.",
    "bekas": "Untuk menyamarkan bekas jerawat kemerahan (*PIE*), gunakan bahan penenang seperti Centella Asiatica, Niacinamide, atau Allantoin. Sedangkan untuk bekas jerawat kehitaman (*PIH*), Anda bisa menggunakan bahan aktif pencerah yang aman seperti Alpha Arbutin, Vitamin C, atau Azelaic Acid.",
    "eksfoliasi": "Eksfoliasi kulit berjerawat sebaiknya menggunakan eksfoliator kimiawi (*chemical exfoliant*) seperti BHA (Salicylic Acid) karena mampu larut dalam minyak dan masuk membersihkan pori-pori dari dalam. Hindari penggunaan scrub fisik kasar (*physical scrub*) karena dapat membuat jerawat pecah dan menyebarkan infeksi.",
    "default": "Terima kasih atas pertanyaan Anda. Untuk permasalahan kulit wajah khususnya jerawat, sangat disarankan menjaga kebersihan wajah dengan double cleansing, menghindari makanan manis/berminyak, memakai obat totol yang mengandung Sulfur/Benzoyl Peroxide, serta rutin menggunakan tabir surya di pagi hari."
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
# 6. INITIALIZE SESSION STATE
# ==========================================
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "image_source" not in st.session_state:
    st.session_state.image_source = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

# ==========================================
# 7. MEDICIO HEADER SYSTEM (image_a953c4.jpg)
# ==========================================
st.markdown("""
    <div class="medicio-top-bar">
        <div class="top-bar-left">
            <span>🕒 Senin - Sabtu, 08:00 - 22:00</span>
            <span>🏫 Universitas PGRI Sumatera Barat</span>
        </div>
        <div class="top-bar-right">
            <span>👤 Hikary Jaidil Zaky (2026)</span>
            <span>📱 Sistem Cerdas Kelas A</span>
        </div>
    </div>
    
    <div class="medicio-brand-bar">
        <div class="brand-logo-container">
            <div class="brand-emblem"></div>
            <div class="brand-title">ACNECARE<span>AI</span></div>
        </div>
        <div class="brand-nav">
            <span class="brand-nav-item active">Home</span>
            <span class="brand-nav-item">Services</span>
            <span class="brand-nav-item">Departments</span>
            <span class="brand-nav-item">Doctors</span>
            <span class="brand-nav-item">Contact</span>
        </div>
        <div>
            <button class="brand-btn">Make an Appointment</button>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 8. SIDEBAR CONTROL PANEL
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2854/2854101.png", width=95)
st.sidebar.markdown("<h2 style='margin-top:10px; color:#2c4964; font-weight:800;'>AcneCare System</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size:13px; color:#64748B; margin-bottom:20px;'>Dermatological Expert Portal</p>", unsafe_allow_html=True)

menu = st.sidebar.radio("PILIH LAYANAN UTAMA:", ["🔎 Deteksi Jerawat AI", "💬 Tanya Jawab Chatbot"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🌐 Tautan Aplikasi Cloud")
st.sidebar.info("Aplikasi dideploy otomatis ke server cloud public.")
st.sidebar.code("https://acnecare-ai.streamlit.app/")

# ==========================================
# MENU 1: DETEKSI JERAWAT AI
# ==========================================
if menu == "🔎 Deteksi Jerawat AI":
    st.markdown("""
        <div class="medicio-hero-section">
            <div class="medicio-hero-card">
                <h1>Welcome to AcneCare AI</h1>
                <p>Medicine made with care. Unggah foto keluhan kulit Anda atau ambil secara real-time untuk klasifikasi tingkat keparahan jerawat menggunakan Jaringan Saraf Konvolusional (CNN) secara akurat, instan, dan aman.</p>
                <div class="medicio-hero-btn">Deep Learning CNN Classifier</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 5], gap="large")
    
    with col1:
        st.markdown("<h3 style='color:#2c4964; font-weight:700;'>📸 Ambil & Unggah Gambar</h3>", unsafe_allow_html=True)
        src_option = st.radio("Pilih Metode Pengambilan:", ["Unggah File Gambar", "Gunakan Kamera Wajah"])
        
        temp_img = None
        if src_option == "Unggah File Gambar":
            temp_img = st.file_uploader("Pilih file gambar wajah (JPG, JPEG, PNG)...", type=["jpg", "jpeg", "png"])
        else:
            temp_img = st.camera_input("Posisikan wajah Anda pada kamera")
            
        if temp_img is not None:
            if st.session_state.uploaded_image != temp_img:
                st.session_state.uploaded_image = temp_img
                st.session_state.image_source = src_option
                st.session_state.prediction_result = None
            
    with col2:
        st.markdown("<h3 style='color:#2c4964; font-weight:700;'>📊 Laporan Hasil Deteksi</h3>", unsafe_allow_html=True)
        
        if st.session_state.uploaded_image is not None:
            try:
                image = Image.open(st.session_state.uploaded_image)
                st.image(image, caption="Citra Wajah Masukan", use_container_width=True)
                
                st.write("")
                if st.button("Mulai Deteksi Jerawat"):
                    with st.spinner("Mengevaluasi gambar dengan jaringan saraf tiruan..."):
                        model = load_acne_model()
                        
                        if model is None:
                            st.error("Model 'model_jerawat_5kelas.keras' gagal dimuat.")
                        else:
                            img_resized = image.resize((224, 224))
                            img_array = np.array(img_resized)
                            if img_array.shape[-1] == 4:
                                img_array = img_array[..., :3]
                            img_array = img_array / 255.0
                            img_array = np.expand_dims(img_array, axis=0)
                            
                            prediction = model.predict(img_array)
                            class_idx = np.argmax(prediction)
                            predicted_class = class_names[class_idx]
                            confidence = np.max(prediction) * 100
                            
                            st.session_state.prediction_result = {
                                "predicted_class": predicted_class,
                                "confidence": confidence,
                                "date": datetime.now().strftime("%d %B %Y - %H:%M")
                            }
                
                if st.session_state.prediction_result is not None:
                    res = st.session_state.prediction_result
                    predicted_class = res["predicted_class"]
                    confidence = res["confidence"]
                    detection_date = res["date"]
                    
                    details = ACNE_DETAILS.get(predicted_class, {
                        "id_name": predicted_class,
                        "severity": "Unknown",
                        "badge_class": "badge-ringan",
                        "desc": "Detail tidak terdefinisi.",
                        "causes": "Unknown.",
                        "solutions": "Consult with a specialist."
                    })
                    
                    # Tampilan diagnosis modern Medicio Style
                    st.markdown(f"""
                        <div class="medicio-result-card">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                                <h3 style="margin:0; color:#2c4964;">🏷️ {details['id_name']}</h3>
                                <span class="badge {details['badge_class']}">{details['severity']}</span>
                            </div>
                            <hr style="border: 0; border-top: 1px solid #E2E8F0; margin: 15px 0;">
                            <p style="font-size:14px; margin: 5px 0; color:#2c4964;"><b>Persentase Keyakinan:</b> {confidence:.2f}%</p>
                            <p style="font-size:14px; margin: 5px 0; color:#2c4964;"><b>Tanggal Diagnosis:</b> {detection_date}</p>
                            <p style="font-size:14px; color:#475569; margin: 15px 0 5px 0; line-height:1.6;"><b>Deskripsi Medis:</b><br>{details['desc']}</p>
                            <p style="font-size:14px; color:#475569; margin: 10px 0 5px 0; line-height:1.6;"><b>Penyebab Utama:</b><br>{details['causes']}</p>
                            <p style="font-size:14px; color:#475569; margin: 10px 0 0 0; line-height:1.6;"><b>Rekomendasi Penanganan:</b><br>{details['solutions']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # FITUR EXPORT 1: DOWNLOAD REPORT (TXT)
                    report_text = f"""==================================================
        LAPORAN DIAGNOSIS KLINIS - ACNECARE AI
==================================================
Tanggal Analisis    : {detection_date}
Jenis Jerawat       : {details['id_name']}
Tingkat Keparahan   : {details['severity']}
Akurasi Prediksi    : {confidence:.2f}%

--------------------------------------------------
DESKRIPSI KONDISI:
{details['desc']}

PENYEBAB UTAMA:
{details['causes']}

SARAN PENANGANAN UTAMA:
{details['solutions']}

--------------------------------------------------
Rencana Perawatan Skincare yang Direkomendasikan:
AM (Pagi Hari):
{chr(10).join(['- ' + r for r in details.get('routine_am', [])])}

PM (Malam Hari):
{chr(10).join(['- ' + r for r in details.get('routine_pm', [])])}

==================================================
Laporan ini dihasilkan secara otomatis oleh sistem kecerdasan buatan.
Silakan konsultasikan dengan dokter spesialis kulit (Sp.DVE) untuk diagnosis klinis lebih lanjut.
© 2026 AcneCare AI - Universitas PGRI Sumatera Barat
"""
                    st.download_button(
                        label="📥 Unduh Laporan Diagnosis (.txt)",
                        data=report_text,
                        file_name=f"Laporan_AcneCare_{predicted_class}.txt",
                        mime="text/plain"
                    )
                    
                    # FITUR EXPORT 2: AM/PM ROUTINE BUILDER
                    st.markdown("""<div class="routine-box">""", unsafe_allow_html=True)
                    st.markdown("<div class='routine-header'>🗓️ AM & PM Acne Routine Builder</div>", unsafe_allow_html=True)
                    st.markdown("<p style='font-size:13px; color:#64748B;'>Centang langkah-langkah skincare harian yang telah Anda lakukan hari ini untuk menjaga barier kulit:</p>", unsafe_allow_html=True)
                    
                    tab_am, tab_pm = st.tabs(["☀️ Rutinitas Pagi (AM)", "🌙 Rutinitas Malam (PM)"])
                    with tab_am:
                        for idx, step in enumerate(details.get("routine_am", [])):
                            st.checkbox(step, key=f"am_step_{idx}")
                    with tab_pm:
                        for idx, step in enumerate(details.get("routine_pm", [])):
                            st.checkbox(step, key=f"pm_step_{idx}")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    if predicted_class == "Cyst":
                        st.warning("⚠️ Jerawat Batu (Cyst) tergolong kondisi berat. Hubungi Dokter Spesialis Kulit (Sp.DVE) untuk penanganan medis lanjutan.")
                                
            except Exception as e:
                st.error(f"Gagal memproses gambar: {str(e)}")
        else:
            st.info("Gunakan opsi input di panel sebelah kiri untuk memproses deteksi jerawat.")

    st.markdown("""
        <div class="medicio-feature-grid">
            <div class="medicio-feature-card">
                <div class="medicio-feature-card-icon">⚡</div>
                <h4>Analisis 1 Detik</h4>
                <p>Model neural network kami menganalisis citra jerawat Anda dalam hitungan detik untuk klasifikasi jenis kulit bermasalah secara langsung.</p>
            </div>
            <div class="medicio-feature-card">
                <div class="medicio-feature-card-icon">🎯</div>
                <h4>Akurasi CNN</h4>
                <p>Arsitektur 3-lapisan konvolusi memastikan ekstraksi parameter klinis dilakukan dengan fokus pada area bengkak dan komedo wajah.</p>
            </div>
            <div class="medicio-feature-card">
                <div class="medicio-feature-card-icon">🔒</div>
                <h4>Privasi Aman</h4>
                <p>Setiap foto dianalisis secara lokal dan riwayat obrolan tidak dikirim ke server luar, menjaga privasi rekam medis Anda seutuhnya.</p>
            </div>
            <div class="medicio-feature-card">
                <div class="medicio-feature-card-icon">🩺</div>
                <h4>Edukasi Mandiri</h4>
                <p>Menyajikan instruksi pengobatan klinis dan rujukan skincare harian yang disesuaikan secara dinamis untuk barier kulit wajah.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# MENU 2: TANYA JAWAB CHATBOT AI
# ==========================================
elif menu == "💬 Tanya Jawab Chatbot":
    st.markdown("""
        <div class="medicio-hero-section" style="background: linear-gradient(135deg, rgba(63,187,192,0.1) 0%, rgba(241,246,254,0.9) 100%), url('https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&q=80&w=1200'); height:220px;">
            <div class="medicio-hero-card" style="padding: 15px 30px; width: 90%;">
                <h1 style="font-size:24px; margin-bottom:5px;">Interaktif Tanya Jawab Kesehatan Kulit</h1>
                <p style="font-size:13px; margin-bottom:0px;">Konsultasikan keluhan kulit atau tanyakan tips seputar jerawat pada asisten lokal kami secara langsung tanpa kuota internet.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_chat, col_info = st.columns([3, 2], gap="large")
    
    with col_chat:
        st.subheader("💬 Ruang Percakapan")
        
        chat_container = st.container()
        with chat_container:
            for chat in st.session_state.chat_history:
                if chat["role"] == "user":
                    st.markdown(f"<div class='chat-bubble user-bubble'><b>Anda:</b><br>{chat['text']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='chat-bubble ai-bubble'><b>AcneCare AI:</b><br>{chat['text']}</div>", unsafe_allow_html=True)
        
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input("Ketik pertanyaan seputar jerawat/skincare Anda...", placeholder="Contoh: bagaimana urutan basic skincare yang benar?")
            submit_button = st.form_submit_button(label="Kirim 🚀")
            
        if submit_button and user_input:
            st.session_state.chat_history.append({"role": "user", "text": user_input})
            
            input_lower = user_input.lower()
            response_text = ""
            
            if "pencet" in input_lower or "tekan" in input_lower or "pecah" in input_lower:
                response_text = CHATBOT_DATABASE["pencet"]
            elif "skincare" in input_lower or "perawatan" in input_lower or "urut" in input_lower:
                response_text = CHATBOT_DATABASE["skincare"]
            elif "batu" in input_lower or "kistik" in input_lower or "bengkak" in input_lower:
                response_text = CHATBOT_DATABASE["batu"]
            elif "makan" in input_lower or "pantangan" in input_lower or "susu" in input_lower or "manis" in input_lower:
                response_text = CHATBOT_DATABASE["makanan"]
            elif "bekas" in input_lower or "merah" in input_lower or "hitam" in input_lower or "noda" in input_lower:
                response_text = CHATBOT_DATABASE["bekas"]
            elif "eksfoliasi" in input_lower or "scrub" in input_lower or "bha" in input_lower or "aha" in input_lower:
                response_text = CHATBOT_DATABASE["eksfoliasi"]
            else:
                response_text = CHATBOT_DATABASE["default"]
                
            st.session_state.chat_history.append({"role": "model", "text": response_text})
            st.rerun()
            
    with col_info:
        st.subheader("💡 Panduan Penanganan Medis")
        st.markdown("<p style='font-size:13.5px; color:#64748B;'>Klik salah satu topik di bawah ini untuk mendapatkan jawaban edukasi instan:</p>", unsafe_allow_html=True)
        
        with st.expander("🚫 Bolehkah memencet jerawat yang sedang meradang?"):
            st.write(CHATBOT_DATABASE["pencet"])
            
        with st.expander("🧴 Bagaimana urutan skincare harian yang benar?"):
            st.write(CHATBOT_DATABASE["skincare"])
            
        with st.expander("🥩 Apa saja makanan yang memicu jerawat?"):
            st.write(CHATBOT_DATABASE["makanan"])
            
        with st.expander("🔥 Bagaimana cara merawat Jerawat Batu yang sakit?"):
            st.write(CHATBOT_DATABASE["batu"])
            
        with st.expander("✨ Bagaimana menghilangkan noda bekas jerawat?"):
            st.write(CHATBOT_DATABASE["bekas"])
            
        with st.expander("🧪 Bagaimana aturan eksfoliasi kulit wajah yang aman?"):
            st.write(CHATBOT_DATABASE["eksfoliasi"])
