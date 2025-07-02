from langchain_core.messages import HumanMessage
from typing import Union, List

def interactive_emotion_conversation(emotion: Union[str, dict], chat_model) -> List[str]:
    """
    基于初始情绪引导用户逐轮表达情绪，用户随时可结束对话，最后由 AI 分析总结。

    参数：
    - emotion: 表情识别结果，可以是 str 或 dict（带置信度）
    - chat_model: 支持 invoke() 的语言模型

    返回：
    - 用户所有回答组成的列表
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

    print("\n🟢 AI 将与您逐轮对话，请回答每个问题，输入“退出”随时结束")

    feedbacks = []
    last_user_input = ""
    max_turns = 10  # 可设置最大轮次，防止过长

    for turn in range(max_turns):
        if turn == 0:
            prompt = (
                f"{emotion_desc}。你是心理咨询师，请提出一个开放式问题，引导用户表达内心感受或压力来源。"
                f"问题要具体、有同理心、避免评判，语言自然。"
            )
        else:
            prompt = (
                f"用户刚才的回答是：{last_user_input}。请根据这个回答提出下一个开放式问题，继续引导用户表达更多。"
                f"问题要具有同理心、具体明确，不要重复之前的问题。"
            )

        response = chat_model.invoke([HumanMessage(content=prompt)])
        question = response.content.strip()

        print(f"\n问题 {turn + 1}：{question}")
        user_input = input("你的回答：").strip()
        if user_input.lower() in ["退出", "exit", "stop", "end"]:
            break
        feedbacks.append(user_input)
        last_user_input = user_input

    return feedbacks
