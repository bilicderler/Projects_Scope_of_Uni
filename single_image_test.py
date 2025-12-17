# import cv2
# import numpy as np
# import joblib
# import pyttsx3

# # ---- MODEL ----
# model = joblib.load("model_2.pkl")

# # ---- TTS ----
# engine = pyttsx3.init()
# engine.setProperty("rate", 150)

# CONFIDENCE_THRESHOLD = 0.40

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

# # ---- GÖRSELİ OKU ----
# image_path = "dataset\\Square\\square (8).jpg"   # test görseli
# img = cv2.imread(image_path)

# if img is None:
#     print("Görsel yüklenemedi!")
#     exit()

# # 🔴 ZORUNLU: 640x480'e sabitle
# img = cv2.resize(img, (480, 360))

# # ---- ÖN İŞLEME ----
# thresh = preprocess(img)

# contours, _ = cv2.findContours(
#     thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
# )

# # ---- KONTUR SEÇ ----
# cnt = None
# for c in sorted(contours, key=cv2.contourArea, reverse=True):
#     area = cv2.contourArea(c)
#     if 1000 < area < 20000:
#         cnt = c
#         break

# if cnt is None:
#     print("Uygun kontur bulunamadı.")
#     exit()

# # ---- ÖZNİTELİK + TAHMİN ----
# hu = hu_log_transform(cnt).reshape(1, -1)

# pred = model.predict(hu)[0]
# prob = np.max(model.predict_proba(hu))

# print(f"Tahmin: {pred} (%{int(prob*100)})")

# # ---- SESLİ OKUMA ----
# if prob >= CONFIDENCE_THRESHOLD:
#     engine.say(pred)
#     engine.runAndWait()

# # ---- GÖRSELLEŞTİR ----
# cv2.drawContours(img, [cnt], -1, (0, 255, 0), 2)
# cv2.putText(
#     img,
#     f"{pred} %{int(prob*100)}",
#     (30, 50),
#     cv2.FONT_HERSHEY_SIMPLEX,
#     1.3,
#     (0, 0, 255),
#     3
# )

# cv2.imshow("Single Image Shape Recognition", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



###########################################################################################################################################################################################
###########################################################################################################################################################################################
###########################################################################################################################################################################################



