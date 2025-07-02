import cv2
import numpy as np
from keras.models import load_model

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# 使用预训练模型 fer2013_mini_XCEPTION
MODEL_PATH = "models/emotion_model.h5"

face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
emotion_classifier = load_model(MODEL_PATH, compile=False)

def analyze_emotion(image_path):
    """
    使用本地 CNN 模型识别面部情绪，并返回 top 情绪及置信度信息

    返回:
        dict {
            "top_emotion": str,
            "score": float,
            "sorted_emotions": List[{"label": str, "score": float}]
        }
    """
    frame = cv2.imread(image_path)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray)

    if len(faces) == 0:
        return {
            "top_emotion": "unknown",
            "score": 0.0,
            "sorted_emotions": []
        }

    x, y, w, h = faces[0]
    roi_gray = gray[y:y + h, x:x + w]
    roi_gray = cv2.resize(roi_gray, (64, 64), interpolation=cv2.INTER_AREA)
    roi = roi_gray.astype("float") / 255.0
    roi = np.expand_dims(roi, axis=-1)
    roi = np.expand_dims(roi, axis=0)

    preds = emotion_classifier.predict(roi)[0]

    sorted_indices = np.argsort(preds)[::-1]
    sorted_emotions = [
        {"label": emotion_labels[i].lower(), "score": float(preds[i])}
        for i in sorted_indices[:3]  # Top-3
    ]

    return {
        "top_emotion": sorted_emotions[0]["label"],
        "score": sorted_emotions[0]["score"],
        "sorted_emotions": sorted_emotions
    }
