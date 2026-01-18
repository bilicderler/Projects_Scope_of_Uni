import cv2
from ultralytics import YOLO
import winsound
import os
import time

# -----------------------------
# AYARLAR
# -----------------------------
MODEL_PATH = "best.pt"
SOUND_DIR = "tts_wav"
CONF_THRESHOLD = 0.25
SPEAK_INTERVAL = 2.0  # saniye

# -----------------------------
# MODEL
# -----------------------------
model = YOLO(MODEL_PATH)

# -----------------------------
# SES KONTROL
# -----------------------------
last_play_time = {}  # label -> time

# -----------------------------
# KAMERA
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # -----------------------------
    # SİYAH - BEYAZ DÖNÜŞÜM
    # -----------------------------
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # YOLO 3 kanal ister → tekrar BGR
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    # -----------------------------
    # YOLO INFERENCE
    # -----------------------------
    results = model(gray_bgr, conf=CONF_THRESHOLD, verbose=False)

    current_time = time.time()

    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            # -----------------------------
            # ÇİZİM (GRAYSCALE ÜZERİNE)
            # -----------------------------
            text = f"{label} %{int(conf * 100)}"

            cv2.rectangle(gray_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.putText(
                gray_bgr,
                text,
                (x1, y1 - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            # -----------------------------
            # SES (WAV)
            # -----------------------------
            last_time = last_play_time.get(label, 0)
            if current_time - last_time >= SPEAK_INTERVAL:
                wav_path = os.path.join(SOUND_DIR, f"{label}.wav")
                if os.path.exists(wav_path):
                    winsound.PlaySound(
                        wav_path,
                        winsound.SND_FILENAME | winsound.SND_ASYNC
                    )
                    last_play_time[label] = current_time

    cv2.imshow("YOLO Detection (Grayscale)", gray_bgr)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
