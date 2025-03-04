import requests
import json


# 定义与 DeepSeek 服务交互的类
class DeepSeekChat:
    def __init__(self, model, base_url):
        self.model = model
        self.base_url = base_url

    def send_message(self, messages):
        # 构建请求数据
        payload = {
            "model": self.model,
            "messages": messages
        }

        headers = {
            "Content-Type": "application/json"
        }

        # 发送请求到本地 DeepSeek 服务
        response = requests.post(self.base_url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            return response.json()  # 返回 DeepSeek 返回的响应
        else:
            return {"error": f"Request failed with status code {response.status_code}"}


# 定义初始化消息
def start_conversation():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}  # 系统消息定义角色
    ]

    # 初始化 DeepSeekChat 实例
    deepseek_chat = DeepSeekChat(
        model="deepseek-r1:1.5b",  # 使用的本地模型
        base_url="http://localhost:11434/v1/chat/completions"  # 本地服务 URL
    )

    while True:
        try:
            # 获取用户输入问题
            user_input = input("You: ")

            # 如果用户输入 "exit" 或按下 Ctrl+C，退出循环
            if user_input.lower() == "exit":
                print("Exiting the conversation.")
                break

            # 添加用户消息
            messages.append({"role": "user", "content": user_input})

            # 发送用户消息并获取模型回答
            response = deepseek_chat.send_message(messages)

            # 检查响应是否包含错误
            if "error" in response:
                print(response["error"])
            else:
                # 打印 DeepSeek 模型的回答
                answer = response.get("choices", [{}])[0].get("message", {}).get("content", "No response")
                print("DeepSeek: " + answer)

        except KeyboardInterrupt:
            print("\nExiting the conversation due to user interrupt.")
            break


if __name__ == "__main__":
    start_conversation()
