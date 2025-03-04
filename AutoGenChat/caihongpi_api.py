import requests
from config import API_KEY  # 从 config.py 导入 API_KEY


def get_caihongpi():
    """
    调用彩虹屁 API，返回一句随机的夸奖话语
    :return: 彩虹屁内容或错误信息
    """
    url = f"https://apis.tianapi.com/caihongpi/index?key={API_KEY}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["code"] == 200:
                return data["result"]["content"]  # 返回彩虹屁内容
            else:
                return f"错误: {data['msg']}"
        else:
            return "请求失败"
    except requests.RequestException as e:
        return f"请求异常: {e}"
