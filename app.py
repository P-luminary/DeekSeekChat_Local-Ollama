import os
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from bs4 import BeautifulSoup
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
import json
from autogen import config_list_from_json
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen import UserProxyAgent
import autogen

# Load environment variables from .env file
load_dotenv()
brwoserless_api_key = os.getenv("BROWSERLESS_API_KEY")
serper_api_key = os.getenv("SERP_API_KEY")
airtable_api_key = os.getenv("AIRTABLE_API_KEY")

# ------------------ 创建自定义代理 ------------------ #
class LocalDeepSeekAssistantAgent(GPTAssistantAgent):
    def __init__(self, name, llm_config):
        # 调整构造函数，确保不使用 OpenAIWrapper
        self.llm_config = llm_config  # 直接传递本地配置
        self.client = None  # 禁用OpenAI的客户端初始化
        super().__init__(
            name=name,
            llm_config=self.llm_config
        )

    def send_request_to_local_deepseek(self, payload):
        response = requests.post(self.llm_config["base_url"], json=payload)
        return response.json() if response.status_code == 200 else None

# ------------------ 创建代理 ------------------ #
# 创建用户代理
user_proxy = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=1,
    code_execution_config={"use_docker": False}
)

# 创建研究者代理（使用本地DeepSeek）
researcher = LocalDeepSeekAssistantAgent(
    name="researcher",
    llm_config={
        "model": "deepseek-r1:1.5b",
        "base_url": "http://localhost:11434/v1/chat/completions"  # 确保使用本地服务的 URL
    }
)
researcher.register_function(
    function_map={
        "web_scraping": web_scraping,
        "google_search": google_search
    }
)

# 创建研究管理代理
research_manager = GPTAssistantAgent(
    name="research_manager",
    llm_config={
        "config_list": [{"model": "deepseek-r1:1.5b", "base_url": "http://localhost:11434/v1/chat/completions"}],
        "timeout": 600
    }
)

# 创建总监代理
director = GPTAssistantAgent(
    name="director",
    llm_config={
        "config_list": [{"model": "deepseek-r1:1.5b", "base_url": "http://localhost:11434/v1/chat/completions"}],
        "timeout": 600
    }
)
director.register_function(
    function_map={
        "get_airtable_records": get_airtable_records,
        "update_single_airtable_record": update_single_airtable_record
    }
)

# 创建群聊
groupchat = autogen.GroupChat(agents=[user_proxy, researcher, research_manager, director], messages=[], max_round=15)
group_chat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": [{"model": "deepseek-r1:1.5b", "base_url": "http://localhost:11434/v1/chat/completions"}]})

# ------------------ 启动对话 ------------------ #
message = """
Research the funding stage/amount & pricing for each company in the list: https://airtable.com/appj0J4gFpvLrQWjI/tblF4OmG6oLjYtgZl/viwmFx2ttAVrJm0E3?blocks=hide
"""
user_proxy.initiate_chat(group_chat_manager, message=message)
