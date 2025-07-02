import os

os.environ["ZHIPUAI_API_KEY"] = "2682966343a29499f372e5ab71a77760.6elLu3bSWGAbZIBO"

os.environ["SERPAPI_API_KEY"] = "e1629960e761804031676af7479d2f3ec594bcf32da3cddd71952aa41d04673c"
os.environ["USER_AGENT"] = ("Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0")

os.environ["OPENAI_API_KEY"] = "sk-UWXqvnoEkoRiG895NYBc7ZK2eWHCM496G63ycYXVgpMQJaFu"
os.environ["OPENAI_URL_BASE"] = "https://api.chatanywhere.tech/v1"

os.environ["IFLYTEK_SPARK_APP_ID"] = "d35cdbb1"
os.environ["IFLYTEK_SPARK_API_KEY"] = "715a8dde4c14b8e8b7910afa968dc719"
os.environ["IFLYTEK_SPARK_API_SECRET"] = "OWVmODVlYjE4MjdmOTI2OWNlZmQxNGVl"
os.environ["IFLYTEK_SPARK_API_URL"] = "wss://spark-api.xf-yun.com/v3.1/chat"
os.environ["IFLYTEK_SPARK_llm_DOMAIN"] = "generalv3"

os.environ["QIANFAN_AK"] = "wJLainTmCaKqJ4I9vlnPDyHQ"
os.environ["QIANFAN_SK"] = "rpNLj9wOlIiyJijQ1qHWf4GqIiMyT4dh"


def get_openai_chat_model():
    from langchain_openai import ChatOpenAI
    chat_model_openai = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    return chat_model_openai


def get_qianfan_chat_model():
    from langchain_community.chat_models import QianfanChatEndpoint
    chat_model_qianfan = QianfanChatEndpoint(
        temperature=0,
        model="ernie-bot-turbo",
        verbose=True,
    )
    return chat_model_qianfan


from langchain_community.chat_models import ChatSparkLLM

from langchain_community.chat_models.sparkllm import ChatSparkLLM

from langchain_community.chat_models.sparkllm import ChatSparkLLM

def get_spark_chat_model():
    chat_model_spark = ChatSparkLLM()
    return chat_model_spark



def get_zhipuai_chat_model():
    from langchain_community.chat_models import ChatZhipuAI
    chat_model_zhipuai = ChatZhipuAI(
        model="glm-4",
        temperature=0.5,
    )
    return chat_model_zhipuai
