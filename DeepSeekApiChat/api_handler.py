# _api_handler.py

from pet_api import get_pet_info
from weather_api import get_weather_info  # 假设你还想处理天气API

# API函数根据关键字进行分类
def handle_api_call(user_input, api_key):
    # 判断用户输入中的关键字，触发相应的API调用
    if "宠物" in user_input:
        return handle_pet_info(user_input, api_key)
    elif "天气" in user_input:
        return handle_weather_info(user_input, api_key)
    else:
        return {"error": "无法识别的请求"}

def handle_pet_info(user_input, api_key):
    pet_name = None
    pet_type = None

    # 根据用户输入识别宠物类型
    if "哈士奇" in user_input or "狗" in user_input:
        pet_name = "哈士奇"
        pet_type = 1  # 犬类
    elif "猫" in user_input:
        pet_type = 0  # 猫科
    # 更多的宠物类型判断...

    # 调用宠物信息API
    return get_pet_info(api_key, pet_name=pet_name, pet_type=pet_type)

def handle_weather_info(user_input, api_key):
    city = "北京"  # 假设从输入中提取城市名称
    return get_weather_info(api_key, city)
