
import pyttsx3
import os

engine = pyttsx3.init()
engine.setProperty("rate", 150)

labels = ["circle", "square", "star", "triangle"]

os.makedirs("tts_wav", exist_ok=True)

# 🔹 TÜM SESLERİ KUYRUĞA AL
for label in labels:
    path = f"tts_wav/{label}.wav"
    print(f"Oluşturuluyor: {path}")
    engine.save_to_file(label, path)

# 🔹 TEK SEFERDE ÇALIŞTIR
engine.runAndWait()

print("✔ Tüm WAV dosyaları başarıyla oluşturuldu")
