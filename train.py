import os
import sys

# Cetak instruksi instan agar user tahu skrip sedang berjalan dan tidak membeku
print("\n" + "="*50)
print("🍀 ACNECARE AI - SKRIP PELATIHAN MODEL")
print("="*50)
print("[1/5] Memulai sistem...")
print("[INFO] Sedang memuat TensorFlow & library pendukung...")
print("[INFO] Proses ini memerlukan waktu 10-40 detik tergantung kecepatan storage Anda. Harap tunggu...\n")

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from sklearn.metrics import classification_report, confusion_matrix

print(f"[OK] TensorFlow berhasil dimuat! (Versi: {tf.__version__})\n")

# ==============================
# PARAMETER & PATH
# ==============================
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 20

# Silakan sesuaikan kembali path folder dataset Anda di bawah ini
TRAIN_DIR = r"C:\Users\Zaky\Documents\SEMESTER 6\PENGEMBANGAN SISTEM CERDAS\archive\AcneDataset\train"
VALID_DIR = r"C:\Users\Zaky\Documents\SEMESTER 6\PENGEMBANGAN SISTEM CERDAS\archive\AcneDataset\valid"
TEST_DIR  = r"C:\Users\Zaky\Documents\SEMESTER 6\PENGEMBANGAN SISTEM CERDAS\archive\AcneDataset\test"

print("[2/5] Membaca direktori dataset...")
for path_name, path_val in [("Train", TRAIN_DIR), ("Valid", VALID_DIR), ("Test", TEST_DIR)]:
    if os.path.exists(path_val):
        print(f"      - Folder {path_name}: Ditemukan ({path_val})")
    else:
        print(f"      - [PERINGATAN] Folder {path_name} TIDAK ditemukan di: {path_val}")

# ==============================
# DATA GENERATOR (AUGMENTASI)
# ==============================
print("\n[3/5] Mempersiapkan Pipeline Augmentasi Gambar...")
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)

valid_datagen = ImageDataGenerator(rescale=1./255)
test_datagen  = ImageDataGenerator(rescale=1./255)

try:
    train_data = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    valid_data = valid_datagen.flow_from_directory(
        VALID_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    test_data = test_datagen.flow_from_directory(
        TEST_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    class_names = list(train_data.class_indices.keys())
    print(f"[OK] Deteksi Kelas Sukses: {class_names}")
    
    # Simpan nama kelas agar sinkron dengan dashboard Streamlit
    with open("class_names.txt", "w") as f:
        f.write("\n".join(class_names))
        
except Exception as e:
    print(f"\n[ERROR] Gagal memuat dataset: {str(e)}")
    print("Silakan periksa kembali path direktori Anda di atas.")
    sys.exit(1)

# ==============================
# STRUKTUR MODEL CNN
# ==============================
print("\n[4/5] Merancang Arsitektur Jaringan Saraf Konvolusional (CNN)...")
model = models.Sequential([
    # Blok Konvolusi 1
    layers.Conv2D(32, (3,3), padding='same', activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    layers.BatchNormalization(),
    layers.MaxPooling2D(2,2),

    # Blok Konvolusi 2
    layers.Conv2D(64, (3,3), padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(2,2),

    # Blok Konvolusi 3
    layers.Conv2D(128, (3,3), padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(2,2),

    # Lapisan Klasifikasi (Fully Connected)
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.5), # Mencegah overfitting
    layers.Dense(len(class_names), activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ==============================
# CONFIG AUTO-SAVE & CALLBACKS
# ==============================
print("\n[5/5] Mengonfigurasi Sistem Auto-Save (Model Checkpoint)...")

# Nama file tujuan penyimpanan model terbaik
# Rekomendasi format modern Keras (.keras). Jika ingin format lama, gunakan (.h5)
model_save_path = "model_jerawat_5kelas.keras" 

# Callback checkpoint untuk menyimpan model dengan akurasi validasi terbaik secara real-time
checkpoint_callback = ModelCheckpoint(
    filepath=model_save_path,
    monitor='val_accuracy',      # Memantau akurasi pada data validasi
    mode='max',                  # Mencari nilai akurasi maksimal
    save_best_only=True,         # Hanya simpan jika akurasinya lebih baik dari epoch sebelumnya
    verbose=1                    # Tampilkan pesan pemberitahuan saat model berhasil disimpan
)

# Callback tambahan untuk menghentikan training lebih cepat jika sudah tidak ada perkembangan
early_stop_callback = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True,
    verbose=1
)

# Mengurangi learning rate secara dinamis jika performa stagnan
reduce_lr_callback = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.2,
    patience=3,
    min_lr=1e-6,
    verbose=1
)

callbacks_list = [checkpoint_callback, early_stop_callback, reduce_lr_callback]

# ==============================
# PROSES TRAINING
# ==============================
print(f"\n🚀 Memulai Pelatihan Model (Epoch Maksimal: {EPOCHS})...")
print(f"Model terbaik otomatis akan disimpan ke file: '{model_save_path}'\n")

history = model.fit(
    train_data,
    validation_data=valid_data,
    epochs=EPOCHS,
    callbacks=callbacks_list
)

# ==============================
# EVALUASI AKHIR
# ==============================
print("\n" + "="*50)
print("📊 EVALUASI AKHIR MODEL")
print("="*50)

# Memuat model terbaik yang baru saja disimpan otomatis
if os.path.exists(model_save_path):
    print(f"[INFO] Memuat kembali model terbaik dari '{model_save_path}' untuk evaluasi...")
    best_model = tf.keras.models.load_model(model_save_path)
else:
    best_model = model

loss, acc = best_model.evaluate(test_data)
print(f"\nAkurasi pada Dataset Uji (Test Accuracy): {acc*100:.2f}%")

# Klasifikasi detail & Confusion Matrix
Y_pred = best_model.predict(test_data)
y_pred = np.argmax(Y_pred, axis=1)

print("\nLaporan Klasifikasi Detail:")
print(classification_report(test_data.classes, y_pred, target_names=class_names))

# Cetak petunjuk akhir ke layar
print("\n" + "="*50)
print("🎉 PROSES SELESAI DENGAN SUKSES!")
print(f"Model siap digunakan pada dashboard Streamlit.")
print(f"Lokasi File Model: {os.path.abspath(model_save_path)}")
print("="*50 + "\n")