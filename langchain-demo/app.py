from flask import Flask, render_template, request, jsonify
from emotion.face_emotion import analyze_emotion
from emotion.emotion_summary import summarize_emotion
from modelchoise import models
from langchain_core.messages import HumanMessage
import base64
import re

app = Flask(__name__)

# 简易用户状态（仅用于原型）
user_session = {
    "emotion": {},
    "feedbacks": [],
    "chat_model": None,
    "last_answer": "",
    "sorted_emotion": []
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start():
    data = request.get_json()
    image_data = data.get('image')
    if not image_data:
        return jsonify({'status': 'fail', 'msg': '没有收到图片数据'})

    # 解析 base64 数据并保存为图片
    img_str = re.sub('^data:image/.+;base64,', '', image_data)
    img_bytes = base64.b64decode(img_str)
    image_path = 'images/face.jpg'
    with open(image_path, 'wb') as f:
        f.write(img_bytes)

    # 后续流程不变
    emotion_result = analyze_emotion(image_path)
    top_emotion = emotion_result.get("top_emotion", "unknown")
    score = emotion_result.get("score", 0.0)
    sorted_emotions = emotion_result.get("sorted_emotions", [])

    if top_emotion == "unknown":
        return jsonify({'status': 'fail', 'msg': '无法识别面部情绪'})

    user_session["emotion"] = {item["label"]: item["score"] for item in sorted_emotions}
    user_session["feedbacks"] = []
    user_session["last_answer"] = ""
    user_session["chat_model"] = models.get_spark_chat_model()
    user_session["sorted_emotions"] = "，".join([
        f"{item['label']}占{round(item['score'] * 100)}%" for item in sorted_emotions
    ])

    prompt = f"观察到用户表现出“{top_emotion}”情绪，请作为心理咨询师，提出一个开放式问题，引导用户表达内心感受。问题要具体、有同理心、避免评判。"
    try:
        response = user_session["chat_model"].invoke([HumanMessage(content=prompt)])
        question = response.content.strip()
    except Exception as e:
        return jsonify({'status': 'fail', 'msg': '生成问题失败，请重试'})

    return jsonify({
        'status': 'ok',
        'emotion': top_emotion,
        'score': round(score, 2),
        'details': sorted_emotions,
        'question': question
    })


@app.route('/next', methods=['POST'])
def next_question():
    data = request.json
    answer = data.get("answer", "").strip()
    if not answer:
        return jsonify({'status': 'fail', 'msg': '没有回答内容'})

    user_session["feedbacks"].append(answer)
    user_session["last_answer"] = answer

    prompt = f"用户刚才回答：“{answer}”，请基于该回答提出下一个开放式问题，引导其进一步表达内心。问题要有共情，不带评判。"
    try:
        response = user_session["chat_model"].invoke([HumanMessage(content=prompt)])
        question = response.content.strip()
    except Exception as e:
        return jsonify({'status': 'fail', 'msg': '生成下一个问题失败，请重试'})

    return jsonify({
        'status': 'ok',
        'question': question
    })


@app.route('/summary', methods=['POST'])
def summary():
    if not user_session["feedbacks"]:
        return jsonify({'status': 'fail', 'msg': '没有回答内容，无法总结'})

    try:
        summary_result = summarize_emotion(
            user_session["feedbacks"],
            user_session["sorted_emotions"],
            user_session["chat_model"]
        )
    except Exception as e:
        return jsonify({'status': 'fail', 'msg': '总结生成失败'})

    return jsonify({'status': 'ok', 'result': summary_result})


if __name__ == '__main__':
    app.run(debug=True)
