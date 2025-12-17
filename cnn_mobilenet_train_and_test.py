
# import cv2
# import os
# import numpy as np
# import joblib

# from sklearn.svm import SVC
# from sklearn.pipeline import make_pipeline
# from sklearn.preprocessing import StandardScaler

# DATASET_PATH = "dataset"

# features = []
# labels = []

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

# for label in os.listdir(DATASET_PATH):
#     class_path = os.path.join(DATASET_PATH, label)

#     for file in os.listdir(class_path):
#         img_path = os.path.join(class_path, file)
#         img = cv2.imread(img_path)

#         if img is None:
#             continue

#         thresh = preprocess(img)
#         contours, _ = cv2.findContours(
#             thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
#         )

#         if not contours:
#             continue

#         # EN UYGUN KONTURU SEÇ
#         cnt = None
#         for c in sorted(contours, key=cv2.contourArea, reverse=True):
#             area = cv2.contourArea(c)
#             if 1000 < area < 20000:
#                 cnt = c
#                 break

#         if cnt is None:
#             continue

#         hu = hu_log_transform(cnt)
#         features.append(hu)
#         labels.append(label)

# X = np.array(features)
# y = np.array(labels)

# model = make_pipeline(
#     StandardScaler(),
#     SVC(kernel="rbf", probability=True)
# )

# model.fit(X, y)

# joblib.dump(model, "model_2.pkl")
# print("✔ Model başarıyla eğitildi ve kaydedildi.")
###########################################################################################################################################################################################
###########################################################################################################################################################################################
###########################################################################################################################################################################################


import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import cv2

# -------------------------------
# AYARLAR
# -------------------------------
DATASET_PATH = "dataset"   # dataset/square, circle, triangle, star
IMG_SIZE = 224
BATCH_SIZE = 8
EPOCHS = 10
CONF_THRESHOLD = 0.60

# -------------------------------
# DATA GENERATOR
# -------------------------------
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=20,
    zoom_range=0.2,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True
)

train_gen = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)

val_gen = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

NUM_CLASSES = train_gen.num_classes
class_names = list(train_gen.class_indices.keys())

# -------------------------------
# MODEL
# -------------------------------
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)

base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation="relu")(x)
outputs = Dense(NUM_CLASSES, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=outputs)

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# -------------------------------
# TRAIN
# -------------------------------
model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS
)

model.save("mobilenet_shapes.h5")
print("✔ Model kaydedildi")

# -------------------------------
# TEK GÖRSEL TEST
# -------------------------------
def predict_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    preds = model.predict(img)[0]
    conf = np.max(preds)
    label = class_names[np.argmax(preds)]

    if conf < CONF_THRESHOLD:
        print("❌ Güven düşük, tahmin edilmedi")
        return

    print(f"✅ Tahmin: {label} (%{int(conf*100)})")

# -------------------------------
# TEST ET
# -------------------------------
predict_image("test.jpg")
