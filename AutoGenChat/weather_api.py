# weather_api.py

import requests

# 假设的天气API获取函数
def get_weather_info(api_key, city):
    url = f"https://apis.tianapi.com/weather/index?key={api_key}&city={city}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["code"] == 200:
            return data["result"]
        else:
            return {"error": f"错误: {data['msg']}"}
    else:
        return {"error": "错误数据返回API"}
