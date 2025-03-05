import requests
from ..config import EXTERNAL_API_KEY

def get_pet_info(pet_name=None, pet_type=None, page=1, num=5):
    """调用天行数据宠物 API 获取宠物信息"""
    url = f"https://apis.tianapi.com/pet/index?key={EXTERNAL_API_KEY}&page={page}&num={num}"

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
