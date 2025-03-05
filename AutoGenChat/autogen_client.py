# autogen_client.py
import openai
import json

from config import DEEPSEEK_API_KEY, DEEPSEEK_API_BASE, DEEPSEEK_MODEL
from AutoGenChat.api_clients.caihongpi_api import get_caihongpi
from AutoGenChat.api_clients.pet_api import get_pet_info

# 配置 OpenAI 客户端
client = openai.OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_API_BASE)

# 定义可以被 AutoGen 调用的函数
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_caihongpi",
            "description": "获取一句彩虹屁",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []  # 确保 API 正确解析
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pet_info",
            "description": "获取宠物信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "pet_name": {"type": "string", "description": "宠物的名称"},
                    "pet_type": {"type": "integer", "description": "宠物类别: 0=猫, 1=狗, 2=爬行类, 3=小宠物, 4=水族"},
                    "page": {"type": "integer", "description": "页码"},
                    "num": {"type": "integer", "description": "获取的宠物数量"}
                },
                "required": ["pet_name", "pet_type"]  # 确保 API 知道哪些参数是必需的
            }
        }
    }
]

def chat_with_autogen(messages):
    """与 AutoGen 进行对话，并让它自动调用 API"""
    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    # 调试输出 response
    print("Response:", response)

    # 解析 AutoGen 返回的 tool_calls
    tool_calls = response.choices[0].message.tool_calls
    if tool_calls:
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            tool_call_id = tool_call.id  # 确保正确获取 tool_call_id

            if function_name == "get_caihongpi":
                result = get_caihongpi()
            elif function_name == "get_pet_info":
                result = get_pet_info(
                    pet_name=function_args.get("pet_name"),
                    pet_type=function_args.get("pet_type"),
                    page=function_args.get("page", 1),
                    num=function_args.get("num", 5)
                )
            else:
                result = "未知函数"

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call_id,  # 关键修复点
                "name": function_name,
                "content": json.dumps(result, ensure_ascii=False)
            })
            return result

    return response.choices[0].message.content
