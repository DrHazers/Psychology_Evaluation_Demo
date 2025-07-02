from flask import Flask, render_template, request, jsonify
from emotion.camera import capture_face_image
from emotion.face_emotion import analyze_emotion
from emotion.question_generator import generate_questions_by_emotion
from emotion.emotion_summary import summarize_emotion
from modelchoise import models

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start():
    # 拍照
    image_path = capture_face_image()

    # 情绪识别（新版 analyze_emotion 返回一个 dict）
    result = analyze_emotion(image_path)

    # 提取主要情绪和置信度
    emotion = result.get("top_emotion", "unknown")
    score = result.get("score", 0.0)

    if emotion == "unknown":
        return jsonify({'status': 'fail', 'msg': '无法识别面部情绪，请重试'})

    # 生成问题
    chat_model = models.get_spark_chat_model()
    questions = generate_questions_by_emotion(emotion, chat_model)

    return jsonify({
        'status': 'ok',
        'emotion': emotion,
        'score': score,
        'questions': questions,
        'details': result.get("sorted_emotions", [])  # 可选返回情绪分布
    })


@app.route('/summary', methods=['POST'])
def summary():
    data = request.json
    feedbacks = data.get('feedbacks', [])
    emotion = data.get('emotion', '')
    chat_model = models.get_spark_chat_model()
    result = summarize_emotion(feedbacks, emotion, chat_model)
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)
