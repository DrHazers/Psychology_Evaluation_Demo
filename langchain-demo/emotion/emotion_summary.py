from langchain_core.messages import HumanMessage


def summarize_emotion(feedbacks: list, emotion: str, chat_model) -> str:
    """
    根据用户回答和面部情绪分布，生成情绪总结与建议。

    参数：
    - feedbacks: 用户的多轮回答列表
    - emotion_summary: 情绪分布字符串，例如 "高兴占72%，中性占18%，愤怒占10%"
    - chat_model: 已初始化的星火对话模型对象

    返回：
    - 分析报告字符串：总结 + 建议
    """
    # 整合所有回答
    joined_feedbacks = "\n".join([
        f"回答{i + 1}：{ans}" for i, ans in enumerate(feedbacks)
    ])

    # 构造 prompt
    prompt = (
        f"根据用户面部表情识别结果，其情绪分布为：{emotion}。\n"
        f"以下是用户的回答内容：\n"
        f"{joined_feedbacks}\n\n"
        f"请你综合以上信息，生成一份简洁的心理情感总结，判断用户是否存在情绪困扰、压力来源，"
        f"并给予温和、具体且具启发性的建议。不要使用医学术语，保持关怀和共情语气。"
    )

    # 调用大模型生成结果
    response = chat_model.invoke([HumanMessage(content=prompt)])
    return response.content
