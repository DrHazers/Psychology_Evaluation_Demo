from modelchoise import models
from emotion.camera import capture_face_image
from emotion.face_emotion import analyze_emotion
from emotion.question_generator import interactive_emotion_conversation
from emotion.emotion_summary import summarize_emotion


def main():
    print("🟢 Step 1：准备拍摄图像，请正对摄像头...")
    image_path = capture_face_image()

    print("\n🟢 Step 2：识别面部情绪中...")
    emotion_result = analyze_emotion(image_path)

    top_emotion = emotion_result.get("top_emotion", "unknown")
    score = emotion_result.get("score", 0.0)
    sorted_emotions = emotion_result.get("sorted_emotions", [])

    if top_emotion == "unknown":
        print("⚠️ 无法识别面部情绪，请重新拍照。")
        return

    # 将 sorted_emotions 列表转为 dict 以支持多情绪描述
    emotion_dict = {label: value for label, value in sorted_emotions}
    print(f"识别到的情绪分布：{emotion_dict}")

    print("\n🟢 Step 3：开始逐轮提问...")
    chat_model = models.get_spark_chat_model()
    feedbacks = interactive_emotion_conversation(emotion_dict, chat_model)

    if not feedbacks:
        print("⚠️ 你没有输入任何回答，无法进行总结。")
        return

    print("\n🟢 Step 4：AI 正在分析你的回答...")
    summary = summarize_emotion(feedbacks, emotion_dict, chat_model)

    print("\n==============================")
    print("🎯 情绪总结与建议：")
    print(summary)
    print("==============================")

if __name__ == "__main__":
    main()
