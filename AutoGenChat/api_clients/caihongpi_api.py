import requests
from ..config import EXTERNAL_API_KEY

def get_caihongpi():
    """调用天行数据的彩虹屁 API，返回一句彩虹屁"""
    url = f"https://apis.tianapi.com/caihongpi/index?key={EXTERNAL_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["code"] == 200:
            return data["result"]["content"]
        else:
            return f"错误: {data['msg']}"
    else:
        return "错误: API 请求失败"
