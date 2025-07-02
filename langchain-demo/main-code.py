from modelchoise import models
from emotion.camera import capture_face_image
from emotion.face_emotion import analyze_emotion
from emotion.question_generator import generate_questions_by_emotion
from emotion.emotion_summary import summarize_emotion

def main():
    print("🟢 Step 1：准备拍摄图像，请正对摄像头...")
    image_path = capture_face_image()

    print("\n🟢 Step 2：识别面部情绪中...")
    emotion_dict = analyze_emotion(image_path)  # 返回字典，如 {'sad': 0.62, 'neutral': 0.20}
    if not emotion_dict:
        print("⚠️ 无法识别面部情绪，请重新拍照。")
        return

    sorted_emotions = sorted(emotion_dict, key=lambda x: x[1], reverse=True)
    top_emotion, top_score = sorted_emotions[0]
    print(f"识别到的主要情绪：{top_emotion}（置信度 {top_score:.2f}）")

    print("\n🟢 Step 3：AI 正在为你生成问题...")
    chat_model = models.get_spark_chat_model()
    questions = generate_questions_by_emotion(emotion_dict, chat_model)

    if not questions:
        print("⚠️ 未能生成问题，请检查模型设置。")
        return

    print("\n请你认真回答以下问题：")
    feedbacks = []
    for i, q in enumerate(questions, 1):
        print(f"问题 {i}：{q}")
        ans = input("你的回答：")
        feedbacks.append(ans)

    print("\n🟢 Step 4：AI 正在分析你的回答...")
    result = summarize_emotion(feedbacks, top_emotion, chat_model)

    print("\n==============================")
    print("🎯 情绪总结与建议：")
    print(result)
    print("==============================")

if __name__ == "__main__":
    main()
