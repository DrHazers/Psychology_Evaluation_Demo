from langchain_core.messages import HumanMessage

def summarize_emotion(feedbacks: list, emotion: str, chat_model) -> str:
    """
    根据用户回答和表情情绪，生成情绪总结与建议。

    参数：
    - feedbacks: 用户回答的问题列表（字符串数组）
    - emotion: 表情识别得到的情绪标签
    - chat_model: 已实例化的对话模型对象

    返回：
    - 分析报告字符串：总结 + 建议
    """
    joined_feedbacks = "\n".join([f"回答{i+1}：{ans}" for i, ans in enumerate(feedbacks)])

    prompt = (
        f"当前用户面部表情识别显示其情绪为“{emotion}”。以下是该用户的文字回答：\n"
        f"{joined_feedbacks}\n"
        f"请根据这些信息，生成一份简洁的心理情感总结，判断该用户是否存在情绪困扰、压力来源，"
        f"并给予适当的建议，语气友善温和，避免诊断术语。"
    )

    response = chat_model.invoke([HumanMessage(content=prompt)])
    return response.content
