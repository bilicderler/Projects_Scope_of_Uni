import cv2
from ultralytics import YOLO
import winsound
import os
import time

# Arduino opsiyonel
try:
    import serial
except ImportError:
    serial = None

# -----------------------------
# AYARLAR
# -----------------------------
MODEL_PATH = "best.pt"
SOUND_DIR = "tts_wav"
CONF_THRESHOLD = 0.25
SPEAK_INTERVAL = 2.0  # saniye
SERIAL_PORT = "COM3"  # Arduino varsa
BAUD_RATE = 9600

# -----------------------------
# MODEL
# -----------------------------
model = YOLO(MODEL_PATH)

# -----------------------------
# ARDUINO GÜVENLİ BAĞLANTI
# -----------------------------
arduino = None
arduino_enabled = False

if serial is not None:
    try:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        arduino_enabled = True
        print("Arduino bağlı ve aktif.")
    except Exception as e:
        print("Arduino bağlı değil, LED devre dışı:", e)

# -----------------------------
# SES KONTROL
# -----------------------------
last_play_time = {}

# -----------------------------
# LED KOMUT HARİTASI
# -----------------------------
LED_COMMANDS = {
    "circle": "C",
    "square": "S",
    "star": "S",
    "triangle": "T"
}

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
    # GRAYSCALE
    # -----------------------------
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    # -----------------------------
    # YOLO
    # -----------------------------
    results = model(gray_bgr, conf=CONF_THRESHOLD, verbose=False)
    current_time = time.time()

    detected_this_frame = False

    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            label = model.names[cls_id].lower()

            detected_this_frame = True

            # -----------------------------
            # ÇİZİM
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
            # SES + LED (KONTROLLÜ)
            # -----------------------------
            last_time = last_play_time.get(label, 0)
            if current_time - last_time >= SPEAK_INTERVAL:
                # SES
                wav_path = os.path.join(SOUND_DIR, f"{label}.wav")
                if os.path.exists(wav_path):
                    winsound.PlaySound(
                        wav_path,
                        winsound.SND_FILENAME | winsound.SND_ASYNC
                    )

                # LED (sadece Arduino varsa)
                if arduino_enabled:
                    try:
                        cmd = LED_COMMANDS.get(label, "N")
                        arduino.write(cmd.encode())
                    except Exception:
                        arduino_enabled = False
                        print("Arduino bağlantısı koptu, LED kapatıldı.")

                last_play_time[label] = current_time

    # -----------------------------
    # HİÇ NESNE YOK → LED OFF
    # -----------------------------
    if not detected_this_frame and arduino_enabled:
        try:
            arduino.write(b"N")
        except Exception:
            arduino_enabled = False

    cv2.imshow("Shape Detection with YOLO (Grayscale)", gray_bgr)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()

if arduino_enabled:
    try:
        arduino.write(b"N")
        arduino.close()
    except Exception:
        pass

cv2.destroyAllWindows()
