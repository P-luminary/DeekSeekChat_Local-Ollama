import requests
import json

# 调用天猫宠物API获取宠物信息
def get_pet_info(api_key, pet_name=None, pet_type=None, page=1, num=5):
    url = f"https://apis.tianapi.com/pet/index?key={api_key}&page={page}&num={num}"

    if pet_name:
        url += f"&name={pet_name}"

    if pet_type is not None:
        url += f"&type={pet_type}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["code"] == 200:
            return data["result"]["list"]
        else:
            return {"error": f"错误: {data['msg']}"}
    else:
        return {"error": "错误数据返回API"}


# 定义与 AutoGen 服务交互的类
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

    def get_pet_info(self, pet_name=None, pet_type=None, page=1, num=5):
        return get_pet_info(self.api_key, pet_name, pet_type, page, num)


# 定义初始化消息
def start_conversation():
    messages = [
        {"role": "system", "content": "You are a helpful assistant who provides clear, concise, and direct answers."}
    ]

    # 初始化AutoGenChat实例
    autogen_chat = AutoGenChat(
        model="deepseek-r1:1.5b",  # 选择AutoGen模型
        base_url="http://localhost:11434/v1/chat/completions",  # 本地服务URL
        api_key="6997598b324200971c1deb2a490deea4"  # 替换为你的API密钥
    )

    while True:
        try:
            # 获取用户输入
            user_input = input("You: ")

            # 如果用户输入 "exit" 或 Ctrl+C，退出循环
            if user_input.lower() == "exit":
                print("Exiting the conversation.")
                break

            # 判断用户是否请求宠物信息
            if "宠物" in user_input:
                pet_name = None
                pet_type = None

                # 根据用户输入识别宠物类型
                if "哈士奇" in user_input or "狗" in user_input:
                    pet_name = "哈士奇"
                    pet_type = 1  # 犬类
                elif "猫" in user_input:
                    pet_type = 0  # 猫科
                elif "爬行" in user_input:
                    pet_type = 2  # 爬行类
                elif "小宠物" in user_input:
                    pet_type = 3  # 小宠物类
                elif "水族" in user_input:
                    pet_type = 4  # 水族类

                pet_info = autogen_chat.get_pet_info(pet_name=pet_name, pet_type=pet_type)

                # 返回宠物信息
                if "error" in pet_info:
                    print(pet_info["error"])
                else:
                    answers = []
                    for pet_details in pet_info:
                    # pet_details = pet_info[0]  # 获取第一个宠物的详细信息
                        answer = f"宠物类型：{pet_details['pettype']}\n" \
                                 f"宠物名称：{pet_details['name']}\n" \
                                 f"宠物英文名：{pet_details['engName']}\n" \
                                 f"性格特点：{pet_details['characters']}\n" \
                                 f"祖籍：{pet_details['nation']}\n" \
                                 f"易患病：{pet_details['easyOfDisease']}\n" \
                                 f"寿命：{pet_details['life']}\n" \
                                 f"价格：{pet_details['price']}\n" \
                                 f"描述：{pet_details['desc']}\n" \
                                 f"体态特征：{pet_details['feature']}\n" \
                                 f"特点：{pet_details['characterFeature']}\n" \
                                 f"照顾须知：{pet_details['careKnowledge']}\n" \
                                 f"喂养注意：{pet_details['feedPoints']}\n" \
                                 f"详细来源：{pet_details['url']}\n" \
                                 f"封面图片：{pet_details['coverURL']}\n"
                        answers.append(answer)
                    # 打印所有宠物的信息
                    print("AutoGen: " + "\n\n".join(answers))

                    # 将所有宠物的信息加入消息列表
                    for answer in answers:
                        messages.append({"role": "assistant", "content": answer})
                    continue

            # 添加用户消息
            messages.append({"role": "user", "content": user_input})

            # 发送用户消息并获取AutoGen生成的响应
            response = autogen_chat.send_message(messages, temperature=0.5, max_tokens=1000)

            # 检查响应是否包含错误
            if "error" in response:
                print(response["error"])
            else:
                # 获取生成的对话内容
                answer = response.get("choices", [{}])[0].get("message", {}).get("content", "No response")
                print("AutoGen: " + answer)

                # 保存AI的回复，继续下一个轮次
                messages.append({"role": "assistant", "content": answer})

        except KeyboardInterrupt:
            print("\nExiting the conversation due to user interrupt.")
            break


if __name__ == "__main__":
    start_conversation()
