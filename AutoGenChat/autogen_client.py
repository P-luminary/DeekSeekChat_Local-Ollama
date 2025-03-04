# autogen_client.py
import openai
import json

from config import API_KEY, DEEPSEEK_API_BASE, DEEPSEEK_MODEL
from AutoGenChat.api_clients.caihongpi_api import get_caihongpi
from AutoGenChat.api_clients.pet_api import get_pet_info

# 配置 OpenAI 客户端
client = openai.OpenAI(api_key=API_KEY, base_url=DEEPSEEK_API_BASE)

# 定义可以被 AutoGen 调用的函数
functions = [
    {
        "name": "get_caihongpi",
        "description": "获取一句彩虹屁",
        "parameters": {}
    },
    {
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
            "required": []
        }
    }
]

def chat_with_autogen(messages):
    """与 AutoGen 进行对话，并让它自动调用 API"""
    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=messages,
        functions=functions
    )

    # 打印 response 和 function_call 来调试
    print("Response:", response)
    function_call = response.choices[0].message.function_call
    if function_call:
        print("Function call detected:", function_call)
        function_name = function_call.name
        function_args = json.loads(function_call.arguments)

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

        # 把 API 响应结果加入对话历史
        messages.append({"role": "function", "name": function_name, "content": json.dumps(result, ensure_ascii=False)})
        return result

    # 返回 AutoGen 的普通对话回复
    return response.choices[0].message.content

