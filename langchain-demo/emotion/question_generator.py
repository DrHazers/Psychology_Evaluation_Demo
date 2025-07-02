from langchain_core.messages import HumanMessage
from typing import Union

def generate_questions_by_emotion(emotion: Union[str, dict], chat_model) -> list:
    """
    根据情绪生成3个开放性问题，引导用户表达情感。

    参数：
    - emotion: 表情识别结果，可以是字符串（单一情绪）或字典（多个情绪及置信度）
        例如 'happy' 或 {'sad': 0.63, 'angry': 0.21}
    - chat_model: 从 model_choice 中获取的语言模型实例

    返回：
    - 问题列表（最多3个）
    """
    if isinstance(emotion, dict):
        sorted_emotions = sorted(emotion.items(), key=lambda x: x[1], reverse=True)
        top_emotion, top_conf = sorted_emotions[0]
        others = ', '.join([f"{k}({v:.2f})" for k, v in sorted_emotions[1:]])
        if others:
            emotion_desc = f"主要情绪是“{top_emotion}”，但也伴随如{others}等情绪"
        else:
            emotion_desc = f"当前表现出“{top_emotion}”的情绪"
    else:
        emotion_desc = f"当前表现出“{emotion}”的情绪"

    prompt = (
        f"{emotion_desc}。请你作为心理咨询师，提出三个开放式问题，引导该人表达内心感受或压力来源。"
        f"问题要具体、有同理心、避免评判，语言要自然。"
    )

    response = chat_model.invoke([HumanMessage(content=prompt)])

    # 提取问题（中英问号 + 简单的序号处理）
    lines = response.content.split('\n')
    questions = []
    for line in lines:
        if "？" in line or "?" in line:
            line_clean = line.strip(" 1234567890.-:：)")
            questions.append(line_clean)

    if not questions:
        questions = [response.content.strip()]  # fallback 全部返回

    return questions[:3]
