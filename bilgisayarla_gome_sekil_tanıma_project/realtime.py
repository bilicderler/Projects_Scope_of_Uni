
# import cv2
# import numpy as np
# import joblib
# import pyttsx3
# import time

# # ---- MODEL ----
# model = joblib.load("model_2.pkl")

# # ---- TTS ----
# engine = pyttsx3.init()
# engine.setProperty("rate", 150)

# # ---- KONTROL DEĞİŞKENLERİ ----
# last_pred = None
# frame_count = 0
# last_speak_time = 0

# CONFIDENCE_THRESHOLD = 0.70   # %70 güven
# FRAME_THRESHOLD = 5           # 5 ardışık frame
# SPEAK_INTERVAL = 3            # saniye

# # ---- GÖRÜNTÜ İŞLEME ----
# def preprocess(img):
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     blur = cv2.medianBlur(gray, 5)
#     _, thresh = cv2.threshold(
#         blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
#     )
#     return thresh

# def hu_log_transform(cnt):
#     moments = cv2.moments(cnt)
#     hu = cv2.HuMoments(moments).flatten()
#     hu = -np.sign(hu) * np.log10(np.abs(hu) + 1e-10)
#     return hu

# # ---- KAMERA ----
# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     thresh = preprocess(frame)
#     contours, _ = cv2.findContours(
#         thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
#     )

#     cnt = None
#     for c in sorted(contours, key=cv2.contourArea, reverse=True):
#         area = cv2.contourArea(c)
#         if 1000 < area < 20000:
#             cnt = c
#             break

#     if cnt is not None:
#         hu = hu_log_transform(cnt).reshape(1, -1)

#         pred = model.predict(hu)[0]
#         prob = np.max(model.predict_proba(hu))

#         # ---- FRAME SAYACI ----
#         if pred == last_pred:
#             frame_count += 1
#         else:
#             frame_count = 1
#             last_pred = pred

#         # ---- SESLİ OKUMA KOŞULLARI ----
#         current_time = time.time()
#         if (
#             prob >= CONFIDENCE_THRESHOLD and
#             frame_count >= FRAME_THRESHOLD and
#             (current_time - last_speak_time) > SPEAK_INTERVAL
#         ):
#             print(f"Sesli okuma: {pred} (%{int(prob*100)})")
#             engine.stop()
#             engine.say(pred)
#             engine.runAndWait()
#             last_speak_time = current_time
#             frame_count = 0

#         # ---- GÖRSEL GERİ BİLDİRİM ----
#         cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
#         cv2.putText(
#             frame,
#             f"{pred} %{int(prob*100)}",
#             (30, 50),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             1.3,
#             (0, 0, 255),
#             3
#         )

#     cv2.imshow("Shape Recognition", frame)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()


###########################################################################################################################################################################################
###########################################################################################################################################################################################
###########################################################################################################################################################################################


import cv2
import numpy as np
import tensorflow as tf
import time
import winsound
import os

# -------------------------------
# AYARLAR
# -------------------------------
TFLITE_MODEL_PATH = "mobilenet_shapes.tflite"
IMG_SIZE = 224
CONF_THRESHOLD = 0.60
SPEAK_INTERVAL = 3.0
ROI_SCALE = 0.6

class_names = ["circle", "square", "star", "triangle"]
TTS_DIR = "tts_wav"

# -------------------------------
# TFLITE MODEL
# -------------------------------
interpreter = tf.lite.Interpreter(model_path=TFLITE_MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

last_spoken_label = None
last_speak_time = 0

# -------------------------------
# KAMERA
# -------------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ✅ AYNA GÖRÜNTÜ
    frame = cv2.flip(frame, 1)

    h, w, _ = frame.shape

    # ---- MERKEZ ROI ----
    roi_w = int(w * ROI_SCALE)
    roi_h = int(h * ROI_SCALE)

    x1 = (w - roi_w) // 2
    y1 = (h - roi_h) // 2
    x2 = x1 + roi_w
    y2 = y1 + roi_h

    roi = frame[y1:y2, x1:x2]

    # ---- MODEL GİRİŞİ ----
    img = cv2.resize(roi, (IMG_SIZE, IMG_SIZE))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    interpreter.set_tensor(input_details[0]["index"], img)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_details[0]["index"])[0]

    conf = float(np.max(preds))
    label = class_names[int(np.argmax(preds))]

    current_time = time.time()

    # ---- SES (KESİN, BLOKLAMAZ) ----
    if conf >= CONF_THRESHOLD:
        if (
            label != last_spoken_label or
            (current_time - last_speak_time) >= SPEAK_INTERVAL
        ):
            wav_path = os.path.join(TTS_DIR, f"{label}.wav")
            if os.path.exists(wav_path):
                winsound.PlaySound(wav_path, winsound.SND_FILENAME | winsound.SND_ASYNC)

            last_spoken_label = label
            last_speak_time = current_time

    # ---- FPS ----
    fps = 1.0 / (current_time - prev_time)
    prev_time = current_time

    # ---- ÇİZİM ----
    color = (0, 255, 0) if conf >= CONF_THRESHOLD else (0, 0, 255)
    text = f"{label} %{int(conf*100)}" if conf >= CONF_THRESHOLD else "Algilaniyor..."

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)

    cv2.putText(frame, text, (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.3, color, 3)

    cv2.putText(frame, f"FPS: {int(fps)}", (30, 95),
                cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 0), 2)

    cv2.imshow("CNN Shape Recognition (Mirror + Stable Audio)", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
