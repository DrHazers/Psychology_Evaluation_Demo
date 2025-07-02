import cv2
import numpy as np
from keras.models import load_model

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# 使用预训练模型 fer2013_mini_XCEPTION（你可以替换为其他模型）
MODEL_PATH = "models/emotion_model.h5"

face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
emotion_classifier = load_model(MODEL_PATH, compile=False)


def analyze_emotion(image_path):
    """
    使用本地 CNN 模型识别面部情绪，并返回 top-3 情绪标签与置信度
    返回:
        List[(情绪标签, 置信度)]，按置信度降序排列
    """
    frame = cv2.imread(image_path)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray)

    if len(faces) == 0:
        return [("unknown", 0.0)]

    x, y, w, h = faces[0]
    roi_gray = gray[y:y + h, x:x + w]
    roi_gray = cv2.resize(roi_gray, (64, 64), interpolation=cv2.INTER_AREA)
    roi = roi_gray.astype("float") / 255.0
    roi = np.expand_dims(roi, axis=-1)
    roi = np.expand_dims(roi, axis=0)

    preds = emotion_classifier.predict(roi)[0]

    # 获取 Top-3 情绪及置信度
    top_indices = preds.argsort()[-3:][::-1]
    top_emotions = [(emotion_labels[i].lower(), float(preds[i])) for i in top_indices]

    return top_emotions

