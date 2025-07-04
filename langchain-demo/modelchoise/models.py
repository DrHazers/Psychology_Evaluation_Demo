import os

os.environ["IFLYTEK_SPARK_APP_ID"] = "d35cdbb1"
os.environ["IFLYTEK_SPARK_API_KEY"] = "715a8dde4c14b8e8b7910afa968dc719"
os.environ["IFLYTEK_SPARK_API_SECRET"] = "OWVmODVlYjE4MjdmOTI2OWNlZmQxNGVl"
os.environ["IFLYTEK_SPARK_API_URL"] = "wss://spark-api.xf-yun.com/v3.1/chat"
os.environ["IFLYTEK_SPARK_llm_DOMAIN"] = "generalv3"


from langchain_community.chat_models import ChatSparkLLM
from langchain_community.chat_models.sparkllm import ChatSparkLLM
from langchain_community.chat_models.sparkllm import ChatSparkLLM

def get_spark_chat_model():
    chat_model_spark = ChatSparkLLM()
    return chat_model_spark


