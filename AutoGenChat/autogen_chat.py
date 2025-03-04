import json
import requests

class AutoGenChat:
    def __init__(self, model, base_url, api_key):
        self.model = model
        self.base_url = base_url
        self.api_key = api_key

    def send_message(self, messages, temperature=0.5, max_tokens=100000):
        # 构建AutoGen请求的数据，加入自定义参数temperature和max_tokens
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": 0.9,
            "frequency_penalty": 0.5,
            "presence_penalty": 0.5
        }

        headers = {
            "Content-Type": "application/json"
        }

        # 发送请求到本地AutoGen服务
        response = requests.post(self.base_url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            return response.json()  # 返回模型生成的结果
        else:
            return {"error": f"Request failed with status code {response.status_code}"}
