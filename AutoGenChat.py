import requests
from autogen import ConversableAgent, GroupChat, GroupChatManager
import json


# DeepSeek 服务交互类
class DeepSeekChat:
    def __init__(self, model, base_url):
        self.model = model
        self.base_url = base_url

    def send_message(self, messages):
        payload = {
            "model": self.model,
            "messages": messages
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.base_url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Request failed with status code {response.status_code}"}


# **DeepSeek 代理**
class DeepSeekAgent(ConversableAgent):
    def __init__(self, model, base_url):
        super().__init__(name="DeepSeekAgent")
        self.chat = DeepSeekChat(model, base_url)

    def generate_reply(self, messages, sender):
        response = self.chat.send_message(messages)
        return response.get("choices", [{}])[0].get("message", {}).get("content", "No response")


# **用户代理**
class UserAgent(ConversableAgent):
    def __init__(self):
        super().__init__(name="UserAgent")

    def generate_reply(self, messages, sender):
        # 处理消息生成回复
        if messages:
            last_message = messages[-1]['content']  # 获取最后的消息
            return f"你说的是：{last_message}"  # 回复用户消息
        return "请重新提问。"  # 如果没有收到消息，给出默认回答



# **创建群聊**
group_chat = GroupChat(
    agents=[DeepSeekAgent(model="deepseek-r1:1.5b", base_url="http://localhost:11434/v1/chat/completions"), UserAgent()],
    speaker_selection_method="round_robin",  # 轮询发言者
    select_speaker_auto_llm_config={"config_list": [{"model": "gpt-3.5-turbo"}]}  # 这个参数要放到 GroupChat
)

# **创建 GroupChatManager**
group_chat_manager = GroupChatManager(groupchat=group_chat)


# 启动对话
def start_conversation():
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Exiting the conversation.")
                break

            response = group_chat_manager.initiate_chat(
                messages=[{"role": "user", "content": user_input}],
                recipient=group_chat.agents[0]  # 发送给 DeepSeekAgent
            )

            print(f"DeepSeek: {response}")

        except KeyboardInterrupt:
            print("\nExiting the conversation due to user interrupt.")
            break


if __name__ == "__main__":
    start_conversation()
